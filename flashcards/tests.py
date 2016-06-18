from django.test import TestCase
from django.core.urlresolvers import resolve
from flashcards.views import home_page
from django.http import HttpRequest
from flashcards.models import Deck

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

class DeckTests(TestCase):

    def test_adding_a_new_deck(self):
        self.assertFalse(Deck.objects.all())
        # add_new_Deck(request, content)
