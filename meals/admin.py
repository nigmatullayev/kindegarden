from .models import MealServingLog
from django.contrib import admin

@admin.register(MealServingLog)
class MealServingLogAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'served_at', 'portions')
    list_filter = ('recipe', 'user', 'served_at')
    search_fields = ('recipe__name', 'user__username')
