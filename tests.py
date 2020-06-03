import time

from selenium import webdriver

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.utils import timezone

from blog.models import Post

BASE_URL = 'http://localhost:8000'

class HomePageTest(TestCase):

    @classmethod
    def setUpClass(self):
        self.test_user = User.objects.create_user(username='testuser', password='12345')
        self.browser = webdriver.Firefox()
        self.browser.get(BASE_URL)

    @classmethod
    def tearDownClass(self):
        self.browser.quit()
        self.test_user.delete()

    def setUp(self):
        self.login = self.client.login(username='testuser', password='12345')

    def tearDown(self):
        pass

    def skip(self, reason):
        print("\n" + reason)
        self.skipTest(reason)

    def test_banner_title_correct(self):
        self.assertIn("lja781 Blog", self.browser.title)

    def test_has_link_to_home_page(self):
        pg_header = self.browser.find_element_by_class_name("page-header")
        home_link = pg_header.find_element_by_link_text('lja781 Blog')
        self.assertEqual(home_link.get_attribute('href'), BASE_URL + "/")

    def test_has_new_post_button(self):
        pg_header = self.browser.find_element_by_class_name("page-header")
        new_doc_link = pg_header.find_element_by_class_name("top-menu")
        self.assertEqual(new_doc_link.get_attribute('href'), BASE_URL + "/post/new/")

class HomePageEmptyTest(TestCase):

    @classmethod
    def setUpClass(self):
        self.test_user = User.objects.create_user(username='testuser', password='12345')
        self.browser = webdriver.Firefox()
        self.browser.get(BASE_URL)

    @classmethod
    def tearDownClass(self):
        self.browser.quit()
        self.test_user.delete()

    def setUp(self):
        self.login = self.client.login(username='testuser', password='12345')

    def tearDown(self):
        pass

    def test_no_posts_message(self):
        pg_content = self.browser.find_element_by_class_name("content")
        posts = pg_content.find_elements_by_class_name("post")
        if (len(posts) != 0):
            self.skip("Post list is not empty")
        self.fail("not yet implemented test")

class HomePageContentTest(TestCase):

    @classmethod
    def setUpClass(self):
        self.test_user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(author = self.test_user, title = "TTILE1", text = "CONTENT1", created_date = timezone.now(), published_date = timezone.now())
        self.browser = webdriver.Firefox()
        self.browser.get(BASE_URL)

    @classmethod
    def tearDownClass(self):
        self.browser.quit()
        self.test_user.delete()

    def setUp(self):
        self.login = self.client.login(username='testuser', password='12345')

    def tearDown(self):
        pass

    def test_posts_exist(self):
        pg_content = self.browser.find_element_by_class_name("content")
        posts = pg_content.find_elements_by_class_name("post")
        print(Post.objects.count())
        if (len(posts) == 0):
            self.fail("Unable to add test post to database")
        else:
            print("Success adding post")
        self.fail("not yet implemented test")
