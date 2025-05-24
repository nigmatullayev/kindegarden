from django.test import TestCase
from meals.models import MealServingLog
from recipes.models import Recipe, RecipeIngredient
from inventory.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

class MealServingLogTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="zafar")
        self.recipe = Recipe.objects.create(name="Manti")
        self.product = Product.objects.create(
            name="Go'sht", quantity=1000, delivery_date="2025-01-01", min_threshold=100
        )
        RecipeIngredient.objects.create(
            recipe=self.recipe, product=self.product, quantity=250
        )
        self.log = MealServingLog.objects.create(
            recipe=self.recipe, user=self.user, portions=3
        )

    def test_recipe_link(self):
        self.assertEqual(self.log.recipe.name, "Manti")

    def test_user_link(self):
        self.assertEqual(self.log.user.username, "zafar")

    def test_portions(self):
        self.assertEqual(self.log.portions, 3)

    def test_served_at_auto(self):
        self.assertIsNotNone(self.log.served_at)

    def test_str(self):
        self.assertIn("Manti", str(self.log))
