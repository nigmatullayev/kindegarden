from django.db import models
from inventory.models import Product

# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название рецепта')

    def __str__(self):
        return self.name

    def possible_portions(self):
        min_portions = None
        for ingredient in self.ingredients.all():
            if ingredient.quantity == 0:
                continue
            available = ingredient.product.quantity // ingredient.quantity
            if min_portions is None or available < min_portions:
                min_portions = available
        return min_portions if min_portions is not None else 0

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients', verbose_name='Рецепт')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(verbose_name='Количество (граммы)')

    def __str__(self):
        return f"{self.product.name} для {self.recipe.name} ({self.quantity} г)"
