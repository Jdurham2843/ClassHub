from django.conf.urls import url
from . import views

app_name = 'flashcards'

urlpatterns =[
    url(r'^add_deck/$', views.add_deck, name='add_deck'),
    url(r'^(?P<pk>[0-9]+)/deck/$', views.DeckView.as_view(), name='view_deck'),
    url(r'^(?P<id>[0-9]+)/add_card_menu/$', views.add_card_menu, name='add_card_menu'),
    url(r'^(?P<id>[0-9]+)/add_cards/$', views.add_cards, name='add_cards'),
    url(r'^(?P<id>[0-9]+)/update_card/$', views.update_card, name='update_card'),
    url(r'^(?P<id>[0-9]+)/update_card_view/$', views.update_card_view, name='update_card_view'),
    url(r'^(?P<id>[0-9]+)/update_deck/$', views.update_deck, name='update_deck'),
    url(r'^(?P<id>[0-9]+)/delete_card/$', views.delete_card, name='delete_card'),
    url(r'^delete_deck/$', views.delete_deck, name='delete_deck'),
]

'''url(r'^(?P<id>[0-9]+)/deck/$', views.view_deck, name='view_deck'),'''
