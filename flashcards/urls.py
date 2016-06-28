from django.conf.urls import url
from . import views

app_name = 'flashcards'

urlpatterns =[
    url(r'^add_deck/$', views.add_deck, name='add_deck'),
    url(r'^(?P<id>[0-9]+)/deck/$', views.view_deck, name='view_deck'),
]
