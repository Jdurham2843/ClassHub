from django.test import TestCase
from django.core.urlresolvers import resolve
from flashcards.views import home_page
from django.http import HttpRequest
from flashcards.models import Deck

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

class DeckAndCardTests(TestCase):

    def test_can_save_and_retrieve_Decks_and_Cards(self):
        deck_0 = Deck.objects.create(title='Deck #1')
        deck_0.save()

        deck_1 = Deck.objects.create(title='Deck #2')
        deck_1.save()

        saved_decks = Deck.objects.all()
        saved_deck_0 = saved_decks[0]
        saved_deck_1 = saved_decks[1]

        self.assertEqual(saved_deck_0.title, 'Deck #1')
        self.assertEqual(saved_deck_1.title, 'Deck #2')

    def test_can_retrieve_html_for_deck_page(self):
        Deck.objects.create(title='New Deck #1')
        self.assertEqual(Deck.objects.count(), 1)
        deckid = Deck.objects.first().id

        response = self.client.post(
            '/flashcards/' + str(deckid) + '/deck/',
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('New Deck #1', response.content.decode())

class NewDeckTest(TestCase):

    def test_can_save_a_POST_request_for_a_new_deck(self):
        response = self.client.post(
            '/flashcards/add_deck/',
            data={'add-deck-title': 'Deck #1'}
        )

        self.assertEqual(Deck.objects.count(), 1)
        new_deck = Deck.objects.first()
        self.assertEqual(new_deck.title, 'Deck #1')

    def test_redirects_to_home_page(self):
        response = self.client.post(
            'flashcards/add_deck/',
            data={'add-deck-title': 'Deck #1'}
        )

        self.assertRedirects(response, '/')
