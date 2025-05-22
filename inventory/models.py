from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название продукта')
    quantity = models.PositiveIntegerField(verbose_name='Количество (граммы)')
    delivery_date = models.DateField(verbose_name='Дата поставки')
    min_threshold = models.PositiveIntegerField(verbose_name='Минимальный порог (граммы)')

    def __str__(self):
        return self.name

class Notification(models.Model):
    message = models.CharField(max_length=512, verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь (если персонально)')

    def __str__(self):
        return self.message
