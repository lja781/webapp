from django.test import TestCase
from django.urls import resolve

from django.contrib.auth.models import User

from .views import post_list
from .models import Post


class PageTests(TestCase):

    @classmethod
    def setUpClass(self):
        self.user = User.objects.create_user(username="test")
        self.user.set_password("12345")
        self.user.save()
        post = Post.objects.create(author=self.user, title="test post", text="test content")

    @classmethod
    def tearDownClass(self):
        self.user.delete()

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
