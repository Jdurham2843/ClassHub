from django.conf.urls import url
from . import views

app_name = 'flashcards'

urlpatterns =[
    url(r'^add_deck/$', views.CreateDeckView.as_view(), name='add_deck'),
    url(r'^(?P<pk>[0-9]+)/deck/$', views.DeckView.as_view(), name='view_deck'),
    url(r'^(?P<pk>[0-9]+)/add_cards/$', views.AddCardView.as_view(), name='add_cards'),
    url(r'^(?P<pk>[0-9]+)/update_card/$', views.UpdateCardView.as_view(), name='update_card'),
    url(r'^(?P<pk>[0-9]+)/update_deck/$', views.UpdateDeckView.as_view(), name='update_deck'),
    url(r'^(?P<pk>[0-9]+)/delete_card/$', views.DeleteCardView.as_view(), name='delete_card'),
    url(r'^delete_deck/$', views.DeleteDeckView.as_view(), name='delete_deck'),
]
