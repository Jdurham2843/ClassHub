from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from flashcards.models import Deck, Card
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class IndexView(generic.ListView):
    template_name = 'flashcards/home.html'
    context_object_name = 'decks'

    def get_queryset(self):
        return Deck.objects.all()

class CreateDeckView(CreateView):
    def post(self, request):
        if request.POST.get('add-deck-title').strip():
            Deck.objects.create(title=request.POST.get('add-deck-title'))
        return redirect('/')

class DeckView(generic.ListView):
    template_name = 'flashcards/deckview.html'

    def get(self, request, pk):
        deck = Deck.objects.get(pk=pk)
        cards = Card.objects.filter(_deck=deck)
        return render(request, self.template_name, {'deck': deck,
            'cards': cards})

class UpdateDeckView(UpdateView):
    def post(self, request, pk):
        deck = Deck.objects.get(pk=pk)
        new_title = request.POST.get('deck-title', False)

        if new_title.strip():
            deck.title = new_title
            deck.save()

        return redirect('/flashcards/' + str(pk) +'/deck/')

class DeleteDeckView(DeleteView):
    def post(self, request):
        check_list = request.POST.getlist('checks[]', False)
        if check_list:
            for item in check_list:
                deck = Deck.objects.get(pk=item)
                Card.objects.filter(_deck=deck).delete()
                deck.delete()
        return redirect('/')

class AddCardView(CreateView):
    def get(self, request, pk):
        deck = Deck.objects.get(pk=pk)
        return render(request, 'flashcards/addcardmenu.html', {'deck': deck})

    def post(self, request, pk):
            deck = Deck.objects.get(pk=pk)

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
                if front_side.strip() and back_side.strip():
                    Card.objects.create(frontside=front_side, backside=back_side,
                        _deck=deck)

            return redirect('/flashcards/' + str(pk) +'/deck/')

class UpdateCardView(UpdateView):
    def get(self, request, pk):
        card = Card.objects.get(pk=pk)
        return render(request, 'flashcards/updatecard.html', {'card': card})

    def post(self, request, pk):
        card = Card.objects.get(pk=pk)
        frontside = request.POST.get('front-side', False)
        backside = request.POST.get('back-side', False)

        if frontside.strip() and backside.strip():
            card.frontside = frontside
            card.backside = backside
            card.save()

        return redirect('/flashcards/' + str(card._deck.pk) +'/deck/')

class DeleteCardView(DeleteView):
    def post(self, request, pk):
        check_list = request.POST.getlist('checks[]', False)
        if check_list:
            for item in check_list:
                Card.objects.get(pk=int(item)).delete()


        return redirect('/flashcards/' + str(pk) +'/deck/')
