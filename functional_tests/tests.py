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

    def test_can_start_a_deck_and_retrieve_it_later(self):
        # Bob enters the Class Hub Website
        self.browser.get('http://localhost:8000')

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

        self.fail("Finish the test!")
