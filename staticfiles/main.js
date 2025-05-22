document.addEventListener('DOMContentLoaded', function() {
  // Chef видит только форму подачи блюда и рецепты для неё
  if (window.userRole === 'Chef') {
    loadRecipes();
  } else {
    loadProducts();
    loadRecipes();
    loadNotifications();
    renderCharts();
  }
  setupServeMealForm();
  // Скрытие элементов по ролям
  if (window.userRole !== 'Chef' && window.userRole !== 'Admin') {
    document.getElementById('serve-meal-form')?.parentElement?.classList.add('d-none');
  }
  if (window.userRole !== 'Manager' && window.userRole !== 'Admin') {
    document.getElementById('notification-list')?.parentElement?.classList.add('d-none');
  }
});

function loadProducts() {
  fetch('/api/inventory/deliveries/')
    .then(r => r.json())
    .then(data => {
      const list = document.getElementById('product-list');
      list.innerHTML = '';
      data.forEach(p => {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.textContent = `${p.name}: ${p.quantity} кг`;
        list.appendChild(li);
      });
    });
}

function loadRecipes() {
  fetch('/api/recipes/list/')
    .then(r => r.json())
    .then(data => {
      const list = document.getElementById('recipe-list');
      const select = document.getElementById('recipe-select');
      if (list) list.innerHTML = '';
      if (select) select.innerHTML = '';
      data.forEach(r => {
        if (list) {
          const li = document.createElement('li');
          li.className = 'list-group-item';
          li.textContent = `${r.name}: ${r.possible_portions} порций`;
          list.appendChild(li);
        }
        if (select) {
          const option = document.createElement('option');
          option.value = r.id;
          option.textContent = r.name;
          select.appendChild(option);
        }
      });
    });
}

function loadNotifications() {
  fetch('/api/inventory/notifications/')
    .then(r => r.json())
    .then(data => {
      const list = document.getElementById('notification-list');
      list.innerHTML = '';
      data.forEach(n => {
        const li = document.createElement('li');
        li.className = 'list-group-item' + (n.is_read ? '' : ' list-group-item-warning');
        li.textContent = `${n.message} (${n.created_at})`;
        list.appendChild(li);
      });
    });
}

function setupServeMealForm() {
  const form = document.getElementById('serve-meal-form');
  if (!form) return;
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    const recipeId = document.getElementById('recipe-select').value;
    const portions = document.getElementById('portions').value;
    fetch('/api/meals/serve/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({ recipe_id: recipeId, portions: portions })
    })
    .then(r => r.json())
    .then(data => {
      document.getElementById('serve-meal-result').textContent = data.detail || 'Готово!';
      loadProducts();
      loadRecipes();
      loadNotifications();
    });
  });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Chart.js
function renderCharts() {
  // График расхода ингредиентов
  fetch('/api/inventory/consumption/')
    .then(r => r.json())
    .then(data => {
      const ctx = document.getElementById('consumptionChart').getContext('2d');
      const labels = data.map(prod => prod.product);
      const values = data.map(prod => prod.consumption[0]?.total_used || 0);
      const barColors = [
        'rgba(220, 38, 38, 0.7)', // ярко-красный
        'rgba(239, 68, 68, 0.7)', // светло-красный
        'rgba(255, 255, 255, 0.7)', // белый
        'rgba(251, 113, 133, 0.7)' // розовый
      ];
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            label: 'Расход',
            data: values,
            backgroundColor: barColors.slice(0, labels.length)
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { labels: { color: '#f5f5f5' } }
          },
          scales: {
            x: { ticks: { color: '#f5f5f5' }, grid: { color: '#444' } },
            y: { ticks: { color: '#f5f5f5' }, grid: { color: '#444' } }
          }
        }
      });
    });
  // График отчётов
  fetch('/api/meals/monthly-report/')
    .then(r => r.json())
    .then(data => {
      const ctx = document.getElementById('reportChart').getContext('2d');
      new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Приготовлено', 'Возможно'],
          datasets: [{
            data: [data.served_portions, data.possible_portions],
            backgroundColor: ['#b22222', '#fff']
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { labels: { color: '#f5f5f5' } }
          }
        }
      });
    });
}

// --- Inventory page logic ---
if (window.location.pathname.startsWith('/inventory')) {
  let inventoryData = [];
  fetch('/api/inventory/deliveries/')
    .then(r => r.json())
    .then(data => {
      inventoryData = data;
      renderInventoryTable(data);
    });
  document.getElementById('inventory-search').addEventListener('input', function() {
    const val = this.value.toLowerCase();
    renderInventoryTable(inventoryData.filter(p => p.name.toLowerCase().includes(val)));
  });
  document.querySelectorAll('#inventory-table th[data-sort]').forEach(th => {
    th.addEventListener('click', function() {
      const key = th.getAttribute('data-sort');
      const sorted = [...inventoryData].sort((a, b) => (a[key] > b[key] ? 1 : -1));
      renderInventoryTable(sorted);
    });
  });
  document.getElementById('export-inventory').addEventListener('click', function() {
    let csv = 'Название,Остаток,Дата поставки,Мин. порог\n';
    inventoryData.forEach(p => {
      csv += `${p.name},${p.quantity||''},${p.delivery_date||''},${p.min_threshold||''}\n`;
    });
    const blob = new Blob([csv], {type: 'text/csv'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'inventory.csv';
    a.click();
  });
}
function renderInventoryTable(data) {
  const tbody = document.querySelector('#inventory-table tbody');
  tbody.innerHTML = '';
  data.forEach(p => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${p.name}</td><td>${p.quantity||''}</td><td>${p.delivery_date||''}</td><td>${p.min_threshold||''}</td>`;
    tbody.appendChild(tr);
  });
}

// --- Reports page logic ---
if (window.location.pathname.startsWith('/reports')) {
  let reportData = [];
  const monthInput = document.getElementById('report-month');
  // Ограничение выбора месяца только до текущего
  const today = new Date();
  const maxMonth = today.toISOString().slice(0, 7);
  monthInput.max = maxMonth;
  function loadReport() {
    const [year, month] = monthInput.value.split('-');
    fetch(`/api/meals/monthly-report/?year=${year}&month=${month}`)
      .then(r => r.json())
      .then(data => {
        reportData = [data];
        renderReportTable(reportData);
        // Если нет данных — скрыть график, показать сообщение
        const empty = (!data.served_portions && !data.possible_portions);
        document.getElementById('reportChart').parentElement.style.display = empty ? 'none' : '';
        document.getElementById('report-empty-message').style.display = empty ? '' : 'none';
        if (!empty) renderReportChart(data);
      });
  }
  monthInput.addEventListener('change', loadReport);
  document.getElementById('export-report').addEventListener('click', function() {
    let csv = 'Год,Месяц,Приготовлено,Возможно,Отклонение,Флаг\n';
    reportData.forEach(r => {
      csv += `${r.year},${r.month},${r.served_portions},${r.possible_portions},${r.percent_difference},${r.flag}\n`;
    });
    const blob = new Blob([csv], {type: 'text/csv'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'report.csv';
    a.click();
  });
  loadReport();
}
function renderReportTable(data) {
  const tbody = document.querySelector('#report-table tbody');
  tbody.innerHTML = '';
  data.forEach(r => {
    const tr = document.createElement('tr');
    const deviation = Math.abs(r.served_portions - r.possible_portions);
    const deviationPercent = r.percent_difference;
    const deviationTitle = `Отклонение между приготовленными и возможными порциями: ${deviation} (${deviationPercent}%)`;
    const flagTitle = r.flag ? 'Отклонение превышает 15% — требуется внимание!' : '';
    tr.innerHTML = `<td>${r.year}</td>
      <td>${r.month}</td>
      <td>${r.served_portions}</td>
      <td>${r.possible_portions}</td>
      <td title='${deviationTitle}'>${r.percent_difference}</td>
      <td>${r.flag ? `<span title='${flagTitle}'>⚠️</span>` : ''}</td>`;
    tbody.appendChild(tr);
  });
}
function renderReportChart(data) {
  const ctx = document.getElementById('reportChart').getContext('2d');
  if (window._reportChart) window._reportChart.destroy();
  window._reportChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Приготовлено', 'Возможно'],
      datasets: [{
        data: [data.served_portions, data.possible_portions],
        backgroundColor: ['#198754', '#0d6efd']
      }]
    },
    options: { responsive: true }
  });
}

// --- Users page logic ---
if (window.location.pathname.startsWith('/users')) {
  let userData = [];
  fetch('/api/users/')
    .then(r => r.json())
    .then(data => {
      userData = data;
      renderUserTable(data);
    });
  document.getElementById('user-search').addEventListener('input', function() {
    const val = this.value.toLowerCase();
    renderUserTable(userData.filter(u => u.username.toLowerCase().includes(val)));
  });
  document.querySelectorAll('#user-table th[data-sort]').forEach(th => {
    th.addEventListener('click', function() {
      const key = th.getAttribute('data-sort');
      const sorted = [...userData].sort((a, b) => (a[key] > b[key] ? 1 : -1));
      renderUserTable(sorted);
    });
  });
  document.getElementById('export-users').addEventListener('click', function() {
    let csv = 'Имя пользователя,Email,Роль\n';
    userData.forEach(u => {
      csv += `${u.username},${u.email},${u.role}\n`;
    });
    const blob = new Blob([csv], {type: 'text/csv'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'users.csv';
    a.click();
  });
}
function renderUserTable(data) {
  const tbody = document.querySelector('#user-table tbody');
  tbody.innerHTML = '';
  data.forEach(u => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${u.username}</td><td>${u.email}</td><td>${u.role}</td>`;
    tbody.appendChild(tr);
  });
} 