import datetime

from django.db import models


# Create your models here.
class Feature(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField(max_length=1000)


class Author(models.Model):
    author = models.CharField(max_length=100)
    song_name = models.CharField(max_length=100)
    date = models.DateField(default=datetime.date.today, blank=True)
    details = models.TextField(max_length=1000)
