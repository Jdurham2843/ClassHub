from django.test import TestCase
from django.core.urlresolvers import resolve
from flashcards.views import home_page
from django.http import HttpRequest
from flashcards.models import Deck, Card

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
        deck = Deck.objects.first()
        Card.objects.create(frontside='test 1', backside='test 1',
            _deck=deck)

        response = self.client.post(
            '/flashcards/' + str(deck.id) + '/deck/',
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('New Deck #1', response.content.decode())
        self.assertIn('test 1', response.content.decode())
        self.assertIn('test 1', response.content.decode())

    def test_add_card_page_navigates_to_right_template(self):
        Deck.objects.create(title='New Deck #1')
        deckid = Deck.objects.first().id
        response = self.client.get(
            '/flashcards/' + str(deckid) +'/add_card_menu/',
        )

        self.assertIn('Add Cards to New Deck #1', response.content.decode())


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
            '/flashcards/add_deck/',
            data={'add-deck-title': 'Deck #1'}
        )

        self.assertRedirects(response, '/')

    def test_can_update_deck_title(self):
        deck = Deck.objects.create(title='New Title')

        response = self.client.post(
            '/flashcards/' + str(deck.id) + '/update_deck/',
            data = {
                'deck-title': 'New New Title',
            }
        )

        deck = Deck.objects.all()[0]
        self.assertEqual(response.status_code, 302)
        self.assertEqual(deck.title, 'New New Title')

class NewCardTest(TestCase):

    def test_can_add_new_card(self):
        deck = Deck.objects.create()
        card1 = Card.objects.create(frontside='front side 1',
            backside='back side 1', _deck=deck)
        card2 = Card.objects.create(frontside='front side 2',
            backside='back side 2', _deck=deck)

        retrieve_card1 = Card.objects.all()[0]
        retrieve_card2 = Card.objects.all()[1]
        self.assertEqual(retrieve_card1.frontside, 'front side 1')
        self.assertEqual(retrieve_card1.backside, 'back side 1')
        self.assertEqual(retrieve_card2.frontside, 'front side 2')
        self.assertEqual(retrieve_card2.backside, 'back side 2')

    def test_can_add_card_to_deck_from_POST_request(self):
        Deck.objects.create(title='New Deck #1')
        deck = Deck.objects.first()
        response = self.client.post(
            '/flashcards/' + str(deck.id) + '/add_cards/',
            data = {
                'front-side-1': 'card front side 1',
                'back-side-1': 'card back side 1',
                'front-side-2': 'card front side 2',
                'back-side-2': 'card back side 2',
            },
        )

        cards = Card.objects.all()
        self.assertEqual(len(cards), 2)

        self.assertEqual(cards[0].frontside, 'card front side 1')
        self.assertEqual(cards[0].backside, 'card back side 1')
        self.assertEqual(cards[0]._deck, deck)
        self.assertEqual(cards[1].frontside, 'card front side 2')
        self.assertEqual(cards[1].backside, 'card back side 2')
        self.assertEqual(cards[1]._deck, deck)

    def test_can_add_cards_that_are_complete_to_deck_from_POST_request(self):
        Deck.objects.create(title='New Deck #1')
        deck = Deck.objects.first()
        response = self.client.post(
            '/flashcards/' + str(deck.id) + '/add_cards/',
            data = {
                'front-side-1': '',
                'back-side-1': 'card back side 1',
                'front-side-2': 'card front side 2',
                'back-side-2': 'card back side 2',
            },
        )

        cards = Card.objects.all()
        self.assertEqual(len(cards), 1)

        self.assertEqual(cards[0].frontside, 'card front side 2')
        self.assertEqual(cards[0].backside, 'card back side 2')
        self.assertEqual(cards[0]._deck, deck)

    def test_can_update_text_on_card(self):
        deck = Deck.objects.create()
        card = Card.objects.create(frontside='front side 1',
            backside='back side 1', _deck=deck)

        response = self.client.post(
            '/flashcards/' + str(card.id) + '/update_card/',
            data = {
                'front-side': 'change front side 1',
                'back-side': 'change back side 1',
            }
        )

        card = Card.objects.all()[0]

        self.assertEqual(response.status_code, 302)
        self.assertEqual(card.frontside, 'change front side 1')
        self.assertEqual(card.backside, 'change back side 1')
