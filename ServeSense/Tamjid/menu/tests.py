from django.test import TestCase
from django.urls import reverse
from .models import MenuItem  
from decimal import Decimal

class MenuItemModelTest(TestCase):
    def setUp(self):
        MenuItem.objects.create(name="Pizza", price=9.99, available=True)

    def test_menu_item_creation(self):
        item = MenuItem.objects.get(name="Pizza")
        self.assertEqual(item.price, 9.99)
        self.assertTrue(item.available)

class MenuViewsTest(TestCase):
    def setUp(self):
        MenuItem.objects.create(name="Burger", price=5.99, available=True)

    def test_menu_list_view(self):
        response = self.client.get(reverse('menu')) 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Burger")
