from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=30)

class Series(models.Model):
    name = models.CharField(max_length=30)
    genre = models.ManyToManyField(Genre)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_series', blank=True)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField(null=True, blank=True)
    vote_average = models.FloatField()
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    poster_path = models.CharField(max_length=100, null=True)
    backdrop_path = models.CharField(max_length=100, null=True)
    overview = models.TextField(blank=True)

class Review(models.Model):
    content = models.CharField(max_length=200)
    score = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)