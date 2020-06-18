from django.test import TestCase
from django.urls import resolve

from django.contrib.auth.models import User

class PageTests(TestCase):

    @classmethod
    def setUpClass(self):
        self.user = User.objects.create_user(username="test")
        self.user.set_password("12345")
        self.user.save()

    @classmethod
    def tearDownClass(self):
        self.user.delete()

    def setUp(self):
        pass

    def tearDown(self):
        pass
    def test_login_page(self):
        response = self.client.get('/accounts/login/')
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_signup_page(self):
        response = self.client.get('/accounts/signup/')
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_profile_page(self):
        self.client.login(username="test", password="12345")
        response = self.client.get('/accounts/profile/')
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.client.logout()
