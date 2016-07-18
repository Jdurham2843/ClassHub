from django.conf.urls import url
from . import views

from django.contrib.auth.decorators import login_required

app_name = 'flashcards'

urlpatterns =[
    url(r'^$',
        login_required(views.IndexView.as_view()), name='home'),
    url(r'^add_deck/$', login_required(views.CreateDeckView.as_view()), name='add_deck'),
    url(r'^(?P<pk>[0-9]+)/deck/$', login_required(views.DeckView.as_view()), name='view_deck'),
    url(r'^(?P<pk>[0-9]+)/add_cards/$',
        login_required(views.AddCardView.as_view()), name='add_cards'),
    url(r'^(?P<pk>[0-9]+)/update_card/$', login_required(views.UpdateCardView.as_view()), name='update_card'),
    url(r'^(?P<pk>[0-9]+)/update_deck/$', login_required(views.UpdateDeckView.as_view()), name='update_deck'),
    url(r'^(?P<pk>[0-9]+)/delete_card/$', login_required(views.DeleteCardView.as_view()), name='delete_card'),
    url(r'^delete_deck/$', login_required(views.DeleteDeckView.as_view()), name='delete_deck'),
]
