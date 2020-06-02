from selenium import webdriver
import unittest

class BasicTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_eg1(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('lja781 Blog', self.browser.title)

if __name__ == '__main__':
    unittest.main()#warnings='ignore')
