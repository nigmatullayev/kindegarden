from .models import Product, Notification
from django.contrib import admin

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'delivery_date', 'min_threshold')
    search_fields = ('name',)
    list_filter = ('delivery_date',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_at', 'is_read', 'user')
    list_filter = ('is_read', 'created_at')
    search_fields = ('message',)
