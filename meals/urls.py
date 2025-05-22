from django.urls import path
from .views import ServeMealAPIView, MealServingLogListAPIView, MonthlyReportAPIView

urlpatterns = [
    path('serve/', ServeMealAPIView.as_view(), name='serve-meal'),
    path('logs/', MealServingLogListAPIView.as_view(), name='meal-serving-logs'),
    path('monthly-report/', MonthlyReportAPIView.as_view(), name='monthly-report'),
] 