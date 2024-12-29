from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    rating = models.FloatField()
    year = models.IntegerField()
    release_date = models.DateField()
    director = models.CharField(max_length=100, blank=True, null=True)
    actors = models.TextField(blank=True, null=True)
    
    
    