from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from django.test import LiveServerTestCase

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Bob enters the Class Hub Website
        self.browser.get('http://localhost:8000')

        # He notices that there is the word Class Hub in the title
        # of the site
        self.assertIn('Class Hub', self.browser.title)

        self.fail("Finish the test!")
