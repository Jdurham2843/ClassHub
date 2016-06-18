from django.db import models

# Create your models here.

class Deck(models.Model):
    title = models.CharField(max_length=50)
    cardCount = models.IntegerField(default=0)
