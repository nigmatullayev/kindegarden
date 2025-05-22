from django.db import models
from django.contrib.auth import get_user_model
from recipes.models import Recipe

# Create your models here.

class MealServingLog(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    served_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время подачи')
    portions = models.PositiveIntegerField(verbose_name='Количество порций')

    def __str__(self):
        return f"{self.recipe.name} ({self.portions} порций) — {self.served_at:%Y-%m-%d %H:%M}"
