from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
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
    cards = Card.objects.filter(_deck=deck)
    return render(request, 'flashcards/deckview.html', {'deck': deck,
        'cards': cards})

def update_deck(request, id):
    deck = Deck.objects.get(pk=id)
    new_title = request.POST.get('deck-title', False)

    if new_title:
        deck.title = new_title
        deck.save()

    return redirect('/flashcards/' + str(id) +'/deck/')

def delete_deck(request):
    if request.method == "POST":
        check_list = request.POST.getlist('checks[]', False)
        if check_list:
            for item in check_list:
                deck = Deck.objects.get(pk=item)
                Card.objects.filter(_deck=deck).delete()
                deck.delete()
    return redirect('/')

def add_card_menu(request, id):
    deck = Deck.objects.get(pk=id)
    return render(request, 'flashcards/addcardmenu.html', {'deck': deck})

def add_cards(request, id):
    deck = Deck.objects.get(pk=id)

    count = 0
    for key in request.POST.keys():
        if 'back-side' in key or 'front-side' in key:
            count += 1

    request_len = count

    for i in range(1, (request_len // 2) + 1):
        front_key = 'front-side-' + str(i)
        back_key = 'back-side-' + str(i)
        front_side = request.POST.get(front_key, False)
        back_side = request.POST[back_key]
        if front_side and back_side:
            Card.objects.create(frontside=front_side, backside=back_side,
                _deck=deck)

    return redirect('/flashcards/' + str(id) +'/deck/')

def update_card(request, id):
    card = Card.objects.get(pk=id)
    frontside = request.POST.get('front-side', False)
    backside = request.POST.get('back-side', False)

    if frontside and backside:
        card.frontside = frontside
        card.backside = backside
        card.save()

    return redirect('/flashcards/' + str(card._deck.id) +'/deck/')

def update_card_view(request, id):
    card = Card.objects.get(pk=id)
    return render(request, 'flashcards/updatecard.html', {'card': card})


def delete_card(request, id):
    if request.method == "POST":
        check_list = request.POST.getlist('checks[]', False)
        if check_list:
            for item in check_list:
                Card.objects.get(pk=int(item)).delete()


    return redirect('/flashcards/' + str(id) +'/deck/')
