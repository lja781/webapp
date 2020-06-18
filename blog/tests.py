from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from django.contrib.auth.models import User

from .views import post_list
from .models import Post


class PageTests(TestCase):

    @classmethod
    def setUpClass(self):
        user = User.objects.create_user(username="test")
        user.set_password("12345")
        user.save()
        post = Post.objects.create(author=user, title="test post", text="test content")

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        self.client.login(username="test", password="12345")

    def tearDown(self):
        self.client.logout()

    def test_home_page(self):
        response = self.client.get('/blog/')
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_detail_page(self):
        posts = Post.objects.all().values_list('id', flat=True)
        if len(posts) == 0:
            self.fail("No posts exist")
        response = self.client.get('/blog/post/' + str(posts[0]) + '/')
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_edit_page(self):
        posts = Post.objects.all().values_list('id', flat=True)
        if len(posts) == 0:
            self.fail("No posts exist")
        response = self.client.get('/blog/post/' + str(posts[0]) + '/edit/')
        self.assertTemplateUsed(response, 'blog/post_edit.html')

    def test_new_page(self):
        response = self.client.get('/blog/post/new/')
        self.assertTemplateUsed(response, 'blog/post_edit.html')
