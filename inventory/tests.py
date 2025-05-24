from django.test import TestCase
from inventory.models import Product, Notification
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Olma",
            quantity=1000,
            delivery_date=date.today(),
            min_threshold=200
        )

    def test_name(self):
        self.assertEqual(self.product.name, "Olma")

    def test_quantity(self):
        self.assertEqual(self.product.quantity, 1000)

    def test_delivery_date(self):
        self.assertEqual(self.product.delivery_date, date.today())

    def test_min_threshold(self):
        self.assertEqual(self.product.min_threshold, 200)

    def test_str(self):
        self.assertEqual(str(self.product), "Olma")

class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ali")
        self.notification = Notification.objects.create(
            message="Maxsus ogohlantirish",
            user=self.user
        )

    def test_message(self):
        self.assertEqual(self.notification.message, "Maxsus ogohlantirish")

    def test_user_link(self):
        self.assertEqual(self.notification.user.username, "ali")

    def test_is_read_default(self):
        self.assertFalse(self.notification.is_read)

    def test_created_at_auto(self):
        self.assertIsNotNone(self.notification.created_at)

    def test_str(self):
        self.assertEqual(str(self.notification), "Maxsus ogohlantirish")
