from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=30)

class Series(models.Model):
    name = models.CharField(max_length=30)
    genre = models.ManyToManyField(Genre)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_series', blank=True )

class Movie(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=100)
    pubDate = models.DateField()
    director = models.CharField(max_length=100)
    actor = models.CharField(max_length=100)
    userRating = models.FloatField()
    movie_series = models.ForeignKey(Series, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')

class Review(models.Model):
    content = models.CharField(max_length=200)
    score = models.IntegerField()
    movie_review = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)