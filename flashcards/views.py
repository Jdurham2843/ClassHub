from django.shortcuts import render, redirect
from django.http import HttpResponse
from flashcards.models import Deck
from django.core.urlresolvers import reverse

# Create your views here.
def home_page(request):
    decks = Deck.objects.all()
    return render(request, 'flashcards/home.html', {'decks': decks})

def add_deck(request):
    Deck.objects.create(title=request.POST.get('add-deck-title'))
    return redirect('/')
