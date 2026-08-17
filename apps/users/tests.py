from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model
from django.urls import reverse

from decimal import Decimal

User = get_user_model()

class UserTest(APITestCase):
    
    def setUp(self):
        
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.profile_url = reverse('profile')
        self.balance_url = reverse('balance')
        
        self.user_data = {
            'username': 'testusername',
            'email': 'test@example.com',
            'password': 'MyPass123',
            'password_confirm': 'MyPass123'
        }
        
        self.user = User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="Password123!",
            balance=Decimal("100.00")
        )
        
    def test_register(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        
    def test_login(self):
        response = self.client.post(
            self.login_url,
            {
                'username': 'existinguser',
                'password': 'Password123!'
            }
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
    def test_logout(self):
        refresh = RefreshToken.for_user(user=self.user)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        response = self.client.post(
            self.logout_url, 
            {'refresh_token': str(refresh)},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        
        response_reuse = self.client.post(
            self.logout_url, 
            {"refresh_token": str(refresh)}, 
            format='json'
        )
        self.assertEqual(response_reuse.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_get_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.data['username'], self.user.username)
        
    def test_patch_profile(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.patch(
            self.profile_url, 
            {
                'email': 'newemail@yandex.com'
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "newemail@yandex.com")
        
    def test_get_balance(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.balance_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_post_balance(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.balance_url, 
                                    {
                                        'amount': 15
                                    },
                                    format='json'
                                )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], '115.00')
        
        
          
        
