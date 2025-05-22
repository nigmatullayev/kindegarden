from celery import shared_task
from .models import MealServingLog
from recipes.models import Recipe
from inventory.models import Notification
from django.db.models import Sum
from datetime import datetime, timedelta

@shared_task
def generate_monthly_report():
    now = datetime.now()
    year = now.year
    month = now.month - 1 if now.month > 1 else 12
    if now.month == 1:
        year -= 1
    served = MealServingLog.objects.filter(
        served_at__year=year, served_at__month=month
    ).aggregate(total=Sum('portions'))['total'] or 0
    possible = 0
    for recipe in Recipe.objects.all():
        possible += recipe.possible_portions()
    percent = 0
    flag = False
    if possible > 0:
        percent = abs(served - possible) / possible * 100
        flag = percent > 15
        if flag:
            Notification.objects.create(
                message=f'[Автоотчёт] Отклонение между приготовленными и возможными порциями за {month}.{year} составило {round(percent,2)}%',
                user=None
            )
    # Можно добавить сохранение отчёта в отдельную модель, если нужно
    return {
        'year': year,
        'month': month,
        'served_portions': served,
        'possible_portions': possible,
        'percent_difference': round(percent, 2),
        'flag': flag
    } 