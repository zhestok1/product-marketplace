from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.brands.models import BrandProfile
from apps.products.models import Category, Product

User = get_user_model()

class TestProduct(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="seller_user",
            email="seller@example.com",
            password="Password123!"
        )
        self.other_user = User.objects.create_user(
            username="other_user",
            email="other@example.com",
            password="Password123!"
        )

        self.my_brand = BrandProfile.objects.create(
            user=self.user,
            brand_type='OOO',
            name='My Awesome Brand',
            inn='1234567890',
            ogrn='1112223334445'
        )
        self.other_brand = BrandProfile.objects.create(
            user=self.other_user,
            brand_type='IP',
            name='Other Brand',
            inn='0987654321',
            ogrn='5554443332221'
        )

        self.category = Category.objects.create(name="Электроника")

        self.product = Product.objects.create(
            name="Смартфон",
            seller=self.my_brand,
            category=self.category,
            description="Мощный смартфон нового поколения",
            price=Decimal("49999.00"),
            quantity=15
        )

        self.category_list_url = reverse('catalog')
        self.category_detail_url = reverse('category_detail', kwargs={'pk': self.category.pk})
        self.product_detail_url = reverse('product_detail', kwargs={'pk': self.product.pk})
        self.product_create_url = reverse('create', kwargs={'brand_id': self.my_brand.pk})

    def test_get_category_list(self):
        """Любой пользователь может получить список категорий"""
        response = self.client.get(self.category_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        
        self.assertTrue(len(results) > 0, f"Список категорий пуст! Ответ: {response.data}")
        
        category_names = [cat.get('name') for cat in results]
        self.assertIn("Электроника", category_names)

    def test_get_category_detail(self):
        """Любой пользователь может получить детали конкретной категории"""
        response = self.client.get(self.category_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Электроника")

    def test_get_product_detail(self):
        """Любой пользователь может посмотреть детальную страницу товара"""
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Смартфон")
        self.assertEqual(Decimal(response.data['price']), Decimal("49999.00"))

    def test_create_product_success(self):
        """Владелец бренда может успешно создать товар для своего бренда"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            "name": "Ноутбук",
            "description": "Игровой ноутбук",
            "price": "89999.00",
            "quantity": 5
        }
        
        initial_count = Product.objects.count()
        response = self.client.post(self.product_create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), initial_count + 1)
        
        created_product = Product.objects.get(name="Ноутбук")
        self.assertEqual(created_product.seller, self.my_brand)
        self.assertEqual(created_product.quantity, 5)

    def test_create_product_unauthenticated(self):
        """Неавторизованный пользователь не может создать товар"""
        data = {
            "name": "Ноутбук-шпион",
            "description": "Без бренда",
            "price": "1000.00",
            "quantity": 1
        }
        
        response = self.client.post(self.product_create_url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_create_product_for_alien_brand(self):
        """Пользователь не может создать товар для чужого бренда (получает 404)"""
        self.client.force_authenticate(user=self.user)
        
        alien_url = reverse('create', kwargs={'brand_id': self.other_brand.pk})
        
        data = {
            "name": "Попытка взлома",
            "description": "Внедрение",
            "price": "10.00",
            "quantity": 1
        }
        
        response = self.client.post(alien_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)