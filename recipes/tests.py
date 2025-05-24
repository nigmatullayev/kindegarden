from django.test import TestCase
from inventory.models import Product
from recipes.models import Recipe, RecipeIngredient

class RecipeModelTest(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(name="Sho'rva")
        self.product = Product.objects.create(
            name="Sabzi", quantity=300, delivery_date="2025-01-01", min_threshold=50
        )
        self.ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe, product=self.product, quantity=100
        )

    def test_name(self):
        self.assertEqual(self.recipe.name, "Sho'rva")

    def test_possible_portions(self):
        self.assertEqual(self.recipe.possible_portions(), 3)

    def test_str(self):
        self.assertEqual(str(self.recipe), "Sho'rva")

class RecipeIngredientModelTest(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(name="Salat")
        self.product = Product.objects.create(
            name="Bodring", quantity=100, delivery_date="2025-01-01", min_threshold=10
        )
        self.ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe, product=self.product, quantity=50
        )

    def test_quantity(self):
        self.assertEqual(self.ingredient.quantity, 50)

    def test_str(self):
        self.assertIn("Bodring", str(self.ingredient))
