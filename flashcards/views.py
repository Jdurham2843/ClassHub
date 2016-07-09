from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from flashcards.models import Deck, Card
from django.core.urlresolvers import reverse


# Create your views here.
def home_page(request):
    decks = Deck.objects.all()
    return render(request, 'flashcards/home.html', {'decks': decks})

def add_deck(request):
    Deck.objects.create(title=request.POST.get('add-deck-title'))
    return redirect('/')

def view_deck(request, id):
    deck = Deck.objects.get(pk=id)
    return render(request, 'flashcards/deckview.html', {'deck': deck})

def add_card_menu(request, id):
    deck = Deck.objects.get(pk=id)
    return render(request, 'flashcards/addcardmenu.html', {'deck': deck})

def add_cards(request, id):
    deck = Deck.objects.get(pk=id)
    request_len = len(request.POST)

    for i in range(0, request_len // 2):
        front_key = 'front-side-' + str(i + 1)
        back_key = 'back-side-' + str(i + 1)
        front_side = request.POST[front_key]
        back_side = request.POST[back_key]
        if front_side and back_side:
            Card.objects.create(frontside=front_side, backside=back_side,
                _deck=deck)
    return redirect('/')
