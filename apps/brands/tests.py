from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse 
from django.contrib.auth import get_user_model

from decimal import Decimal
from apps.brands.models import BrandProfile

User = get_user_model()

class TestBrandProfile(APITestCase):
    
    def setUp(self):
        
        self.user = User.objects.create_user(
                    username="existinguser",
                    email="existing@example.com",
                    password="Password123!",
                    balance=Decimal("100.00")
                )
        
        brand_1 = BrandProfile.objects.create(
            user = self.user,
            brand_type='OOO', 
            name='Brand Alpha', 
            inn='1234567890', 
            ogrn='1112223334445'
        )
        
        brand_2 = BrandProfile.objects.create(
            user = self.user,
            brand_type='IP', 
            name='Brand Beta', 
            inn='0987654321', 
            ogrn='5554443332221'
        )
        
        brand_3 = BrandProfile.objects.create(
            user=self.user, 
            brand_type='OOO', 
            name='Alien Brand', 
            inn='9999999999', 
            ogrn='9999999999999'
        )
        
        self.brand_list_url = reverse('brand_list')
        self.brand_pk_url = reverse('brand', kwargs={'pk': brand_1.pk})
        self.brand_register_url = reverse('brand_register')
        
    def test_get_brand_list(self):
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.brand_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BrandProfile.objects.count(), 3)
        
    def test_get_brand(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.brand_pk_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Brand Alpha')
        
    def test_brand_create(self):
        self.client.force_authenticate(user=self.user)
        
        data = {
            "user": self.user.pk,
            "brand_type": "OOO",
            "name": "New Wildberries Brand",
            "inn": "7777777777",
            "ogrn": "1234567890123"
        }
        
        response = self.client.post(self.brand_register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BrandProfile.objects.count(), 4)
        new_brand = BrandProfile.objects.get(name="New Wildberries Brand")
        self.assertEqual(new_brand.user, self.user)
        self.assertEqual(new_brand.inn, "7777777777")
        
    