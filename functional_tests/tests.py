import sys
import time

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
        self.browser.get('http://localhost:8081/flashcards/')

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

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Deck #1', body.text)

        # Bob then decides to add a card to his deck
        addCard = self.browser.find_element_by_id('add-card-link')
        addCard.click()
        addCardTitle = self.browser.find_element_by_id('add-card-title')
        self.assertIn('Add Cards to Deck #1', addCardTitle.text)
        frontSide1 = self.browser.find_element_by_id('front-side-1')
        frontSide1.send_keys('front side test 1')
        backSide1 = self.browser.find_element_by_id('back-side-1')
        backSide1.send_keys('back side test 1')
        submitCards = self.browser.find_element_by_id('submit-cards')
        submitCards.click()

        # Bob is redirected to the deck page and see's his new card added
        cardTable = self.browser.find_element_by_tag_name('table')
        self.assertIn('front side test 1', cardTable.text)
        self.assertIn('back side test 1', cardTable.text)

        # Bob decides to add two more cards to his deck
        addCard = self.browser.find_element_by_id('add-card-link')
        addCard.click()
        frontSide2 = self.browser.find_element_by_id('front-side-1')
        frontSide2.send_keys('front side test 2')
        backSide2 = self.browser.find_element_by_id('back-side-1')
        backSide2.send_keys('back side test 2')

        # Bob sees that he can add a third card without having to leave the add card page
        addAnotherCard = self.browser.find_element_by_id('add-another-card')
        addAnotherCard.click()
        addCardForm = self.browser.find_element_by_tag_name('form')

        # Bob adds a third card
        frontSide3 = self.browser.find_element_by_id('front-side-2')
        backSide3 = self.browser.find_element_by_id('back-side-2')
        frontSide3.send_keys('front side test 3')
        backSide3.send_keys('back side test 3')
        submitCards = self.browser.find_element_by_id('submit-cards')

        submitCards.click()

        # Bob is redirected to the Deck page and sees his two new cards added to the page
        cardTable = self.browser.find_element_by_tag_name('table')
        self.assertIn('front side test 1', cardTable.text)
        self.assertIn('back side test 1', cardTable.text)
        self.assertIn('front side test 2', cardTable.text)
        self.assertIn('back side test 2', cardTable.text)
        self.assertIn('front side test 3', cardTable.text)
        self.assertIn('back side test 3', cardTable.text)

        # Bob decides that he would like to update Card 1
        card_1_link = self.browser.find_element_by_id('card-1')
        card_1_link.click()
        front_side = self.browser.find_element_by_id('front-side')
        front_side.clear()
        front_side.send_keys('change to front side')
        back_side = self.browser.find_element_by_id('back-side')
        back_side.clear()
        back_side.send_keys('change to back side')
        update_button = self.browser.find_element_by_id('update-button')
        update_button.click()

        # Bob sees his card updated on the main page
        body_text = self.browser.find_element_by_tag_name('body')
        self.assertIn('change to front side', body_text.text)
        self.assertIn('change to back side', body_text.text)
        self.assertNotIn('front side test 1', body_text.text)
        self.assertNotIn('back side test 1', body_text.text)

        # Bob would also like to update the title of his deck
        change_title_box = self.browser.find_element_by_id('change-deck-title')
        change_title_box.send_keys('New New Deck')
        change_deck_button = self.browser.find_element_by_id('change-deck-button')
        change_deck_button.click()

        # Bob sees the new title of his deck
        deck_title = self.browser.find_element_by_id('deck-title')
        self.assertEquals(deck_title.text, 'New New Deck')

        # Bob decides that he wants to delete a card from his deck
        card_checkbox = self.browser.find_element_by_id('checkbox-1')
        card_checkbox.click()
        card_delete_button = self.browser.find_element_by_id('delete-card-button')
        card_delete_button.click()

        # Bob no longer sees the card in the deck anymore
        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('change to front side', body.text)
        self.assertNotIn('change to back side', body.text)

        # Bob decides that he wants to the delete the deck
        home_link = self.browser.find_element_by_id('home-link')
        home_link.click()

        deck_checkbox_1 = self.browser.find_element_by_id('deck-1-checkbox')
        deck_checkbox_1.click()
        delete_deck_button = self.browser.find_element_by_id('delete-deck-button')
        delete_deck_button.click()

        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('New New Deck', body.text)

        # Bob Logs off
