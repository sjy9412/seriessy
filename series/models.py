from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=30)

class Series(models.Model):
    name = models.CharField(max_length=30)
    genre = models.ManyToManyField(Genre)
    overview = models.TextField(blank=True)
    poster_path = models.CharField(max_length=100, null=True)
    backdrop_path = models.CharField(max_length=100, null=True)
    score_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='score_series', through='Score')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_series', blank=True)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField(null=True, blank=True)
    vote_average = models.FloatField()
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    poster_path = models.CharField(max_length=100, null=True)
    backdrop_path = models.CharField(max_length=100, null=True)
    overview = models.TextField(blank=True)
    story = models.IntegerField(default=0)
    video_url = models.TextField(max_length=200)

class Review(models.Model):
    content = models.CharField(max_length=200)
    score = models.IntegerField()
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Score(models.Model):
    user_score = models.IntegerField()
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Request(models.Model):
    series_name = models.CharField(max_length=100)
    user = models.CharField(max_length=100)