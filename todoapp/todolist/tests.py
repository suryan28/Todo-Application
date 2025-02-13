from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.index_url = reverse('index')
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')

    def test_register_view(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'confirm_password': 'newpassword123'  # Ensure passwords match
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertEqual(User.objects.last().username, 'newuser')

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_logout_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_index_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
