import json

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from flashcards.models import Deck, Card
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_user

def create_login_user(testcase):
    user = User.objects.create_user(username='testuser')
    user.set_password('pass')
    user.save()

    user = authenticate(username=user.username, password='pass')

    response = testcase.client.post(
        '/login/',
        data = {
        'username': user.username,
        'password': 'pass',
        }
    )

    testcase.assertEqual(response.status_code, 302)
    return user


class DeckAndCardTests(TestCase):

    def test_can_save_and_retrieve_Decks_and_Cards(self):
        user = create_login_user(self)
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
        user = create_login_user(self)
        Deck.objects.create(title='New Deck #1', _user=user)
        self.assertEqual(Deck.objects.count(), 1)
        deck = Deck.objects.first()
        Card.objects.create(frontside='test 1', backside='test 1',
            _deck=deck)

        response = self.client.get(
            '/flashcards/' + str(deck.pk) + '/deck/',
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('New Deck #1', response.content.decode())
        self.assertIn('test 1', response.content.decode())
        self.assertIn('test 1', response.content.decode())

    def test_add_card_page_navigates_to_right_template(self):
        user = create_login_user(self)
        Deck.objects.create(title='New Deck #1', _user=user)
        deckid = Deck.objects.first().pk
        response = self.client.get(
            '/flashcards/' + str(deckid) +'/add_cards/',
        )

        self.assertIn('Add Cards to New Deck #1', response.content.decode())

    def test_can_delete_deck_and_all_its_contents(self):
        user = create_login_user(self)
        deck1 = Deck.objects.create(title='title1')
        deck2 = Deck.objects.create(title='title2')
        for i in range(0, 10):
            Card.objects.create(frontside='front', backside='back', _deck=deck1)
            Card.objects.create(frontside='front', backside='back', _deck=deck2)

        self.assertEqual(len(Card.objects.filter(_deck=deck1)), 10)
        self.assertEqual(len(Card.objects.filter(_deck=deck2)), 10)

        response = self.client.post(
            '/flashcards/delete_deck/',
            data = {
                'checks[]': [str(deck1.id), str(deck2.id)]
            }
        )

        self.assertEqual(len(Card.objects.filter(_deck=deck1)), 0)
        self.assertEqual(len(Card.objects.filter(_deck=deck2)), 0)
        self.assertEqual(response.status_code, 302)

class NewDeckTest(TestCase):

    def test_can_save_a_POST_request_for_a_new_deck(self):
        user = create_login_user(self)
        response = self.client.post(
            '/flashcards/add_deck/',
            data={'add-deck-title': 'Deck #1'}
        )

        self.assertEqual(Deck.objects.count(), 1)
        new_deck = Deck.objects.first()
        self.assertEqual(new_deck.title, 'Deck #1')

    def test_redirects_to_home_page(self):
        user = create_login_user(self)
        response = self.client.post(
            '/flashcards/add_deck/',
            data={'add-deck-title': 'Deck #1'}
        )

        self.assertRedirects(response, '/flashcards/')

    def test_can_update_deck_title(self):
        user = create_login_user(self)
        deck = Deck.objects.create(title='New Title')

        response = self.client.post(
            '/flashcards/' + str(deck.id) + '/update_deck/',
            data = {
                'deck-title': 'New New Title',
            }
        )

        deck.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(deck.title, 'New New Title')

class NewCardTest(TestCase):

    def test_can_add_new_card(self):
        user = create_login_user(self)
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
        user = create_login_user(self)
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
        user = create_login_user(self)
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
        user = create_login_user(self)
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

        card.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(card.frontside, 'change front side 1')
        self.assertEqual(card.backside, 'change back side 1')

    def test_can_delete_card_from_deck(self):
        user = create_login_user(self)
        deck = Deck.objects.create(title='title')
        card1 = Card.objects.create(frontside='front', backside='back', _deck=deck)
        card2 = Card.objects.create(frontside='front', backside='back', _deck=deck)
        card3 = Card.objects.create(frontside='front', backside='back', _deck=deck)

        response = self.client.post(
            '/flashcards/' + str(deck.id) + '/delete_card/',
            data = {
                'checks[]': [str(card1.id), str(card2.id), str(card3.id)],
            }
        )

        self.assertFalse(Card.objects.all())

class ReviewTest(TestCase):
    def test_can_get_json_data(self):
        user = create_login_user(self)
        deck = Deck.objects.create(title='new deck', _user=user)
        for i in range(0, 9):
            front_side = 'front side {}'.format(i)
            back_side = 'back side {}'.format(i)
            Card.objects.create(frontside=front_side, backside=back_side,
                _deck=deck)

        response = self.client.get(
            '/flashcards/' + str(deck.pk) + '/review/',
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.context['json_data']))
