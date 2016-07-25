from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Deck(models.Model):
    title = models.CharField(max_length=50)
    cardCount = models.IntegerField(default=0)
    _user = models.ForeignKey(User, null=True)

class Card(models.Model):
    frontside = models.TextField()
    backside = models.TextField()
    _deck = models.ForeignKey('Deck', on_delete=models.CASCADE)
