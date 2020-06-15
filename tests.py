from selenium import webdriver

from unittest import TestCase

'''
Keep these tests independent from Django
'''

BASE_URL = 'http://localhost:8000'
username = 'testuser'
password = '12345'

class HomePageTest(TestCase):

    def skip(self, reason):
        self.skipTest(reason)

    @classmethod
    def setUpClass(self):
        self.browser = webdriver.Firefox()
        self.browser.get(BASE_URL)

    @classmethod
    def tearDownClass(self):
        self.browser.quit()

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

    def test_displays_content_correctly(self):
        pg_content = self.browser.find_element_by_class_name("content")
        posts = pg_content.find_elements_by_class_name("post")
        if (len(posts) > 0):
            post = posts[0]
            pub_date = post.find_element_by_class_name("date")
            self.assertIn("published: ", pub_date.text)
            post_title = post.find_element_by_tag_name("h2 a")
            post_title_link = post_title.get_attribute("href")
            self.assertIn(BASE_URL + "/post/", post_title_link)

            post_content = post.find_element_by_class_name("content-preview")
            self.assertTrue(len(post_content.text) > 0)
        else:
            self.skip("Post list is empty")

    def test_displays_no_content_message_correctly(self):
        pg_content = self.browser.find_element_by_class_name("content")
        posts = pg_content.find_elements_by_class_name("post")
        if (len(posts) == 0):
            notification = pg_content.find_element_by_class_name("inline-notify")
            self.assertEqual(notification.text, "Oh no! There aren't any posts yet!")
        else:
            self.skip("Post list is not empty")
