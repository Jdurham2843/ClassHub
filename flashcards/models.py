from django.db import models

# Create your models here.

class Deck(models.Model):
    title = models.CharField(max_length=50)
    cardCount = models.IntegerField(default=0)

class Card(models.Model):
    frontside = models.TextField()
    backside = models.TextField()
    _deck = models.ForeignKey('Deck', on_delete=models.CASCADE)
