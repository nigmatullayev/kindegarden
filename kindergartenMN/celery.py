import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kindergartenMN.settings')

app = Celery('kindergartenMN')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'generate-monthly-report-every-month': {
        'task': 'meals.tasks.generate_monthly_report',
        'schedule': crontab(minute=0, hour=0, day_of_month=1),
    },
} 