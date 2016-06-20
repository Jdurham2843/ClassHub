import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_deck_and_retrieve_it_later(self):
        # Bob enters the Class Hub Website
        self.browser.get('http://localhost:8081')

        # He notices that there is the word FlashBang in the title
        # of the site and on the page
        self.assertIn('FlashBang', self.browser.title)

        # He sees a form area to add a new flashcard deck
        addDeckButton = self.browser.find_element_by_id('add-deck')
        addDeckTitle = self.browser.find_element_by_id('add-deck-title')

        # Bob enters a title for his new deck, and clicks the button
        addDeckTitle.send_keys('Deck #1')
        addDeckButton.submit()

        # Bob sees his new deck appear
        deckTable = self.browser.find_element_by_tag_name('table').text
        self.assertIn('Deck #1', deckTable)

        # Bob then clicks on Deck #1 and sees the new Deck page
        deckLink = self.browser.find_element_by_id('deck-link-1')
        deckLink.click()

        self.assertIn('Deck #1', self.browser.title)

        self.fail("Finish the test!")
