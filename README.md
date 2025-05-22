# Bog'cha Food and Inventory Management System

Система управления продуктами и инвентарем для детского сада.

## Функциональность

- Управление продуктами и инвентарем
- Управление рецептами
- Система подачи блюд
- Расчет порций
- Визуализация и отчеты
- Отслеживание пользователей
- Ролевой доступ
- Оповещения и уведомления
- Фоновые задачи
- Обновления в реальном времени

## Технический стек

- Backend: Django + Django REST Framework
- Frontend: HTML, CSS, JavaScript
- База данных: MYSQL
- Фоновые задачи: Celery + Redis

## Установка

1. Клонировать репозиторий:
```bash
git clone [url-репозитория]
```

2. Создать виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установить зависимости:
```bash
pip install -r requirements.txt
```

4. Создать файл .env в корневой директории и настроить переменные окружения:
<!-- ```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
``` -->

5. Применить миграции:
```bash
python manage.py migrate
```

6. Создать суперпользователя:
```bash
python manage.py createsuperuser
```

7. Запустить сервер разработки:
```bash
python manage.py runserver
```

## Структура проекта

- `bogcha/` - основной проект Django
- `inventory/` - приложение для управления инвентарем
- `recipes/` - приложение для управления рецептами
- `meals/` - приложение для управления подачей блюд
- `users/` - приложение для управления пользователями
- `reports/` - приложение для отчетов и аналитики

## Роли пользователей

1. Администратор - полный доступ ко всем функциям
2. Повар - только функции подачи блюд
3. Менеджер - обновление инвентаря и аналитика

## Лицензия

MIT 

## Быстрый старт

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Запустите Redis:
   ```bash
   redis-server
   ```
3. Примените миграции:
   ```bash
   python manage.py migrate
   ```
4. (Опционально) Загрузите тестовые данные:
   ```bash
   python manage.py loaddata fixtures/sample_data.json
   ```
5. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```
6. Запустите сервер:
   ```bash
   python manage.py runserver
   ```
7. Запустите Celery worker и beat:
   ```bash
   celery -A kindergartenMN worker --loglevel=info
   celery -A kindergartenMN beat --loglevel=info
   ```

## Роли пользователей
- **Admin** — полный доступ
- **Chef** — только подача блюда и просмотр логов
- **Manager** — инвентарь, отчёты, оповещения

Группы создаются автоматически. Добавляйте пользователей в группы через админку.

## Примеры API
- Подача блюда: `POST /api/meals/serve/` (Chef/Admin)
- Логи подачи: `GET /api/meals/logs/` (Chef/Manager/Admin)
- Ежемесячный отчёт: `GET /api/meals/monthly-report/` (Manager/Admin)
- Список рецептов: `GET /api/recipes/list/` (все роли)
- Расход ингредиентов: `GET /api/inventory/consumption/` (Manager/Admin)
- Оповещения: `GET /api/inventory/notifications/` (Manager/Admin)

## Архитектура
- **inventory/** — продукты, оповещения, аналитика
- **recipes/** — рецепты и ингредиенты
- **meals/** — подача блюда, логи, отчёты, Celery задачи
- **users/** — (опционально) расширение пользователей

## Тестовые данные (fixtures)
Пример файла: `fixtures/sample_data.json`

## Запуск Celery и Redis
- Redis должен быть запущен на `localhost:6379`
- Celery worker и beat запускаются отдельными командами (см. выше)

## Безопасность
- Все API защищены авторизацией и ролевым доступом
- В админке можно управлять пользователями и ролями

## Визуализация и фронтенд
- Для графиков используйте Chart.js или аналогичные библиотеки
- API возвращают данные, готовые для визуализации

## Контакты и поддержка
- Вопросы — через Issues или напрямую разработчику 