from django.shortcuts import render, get_object_or_404, redirect
from .models import Genre, Movie, Review, Series


# Create your views here.

def index(request):
    series = Series.objects.all()
    context = {
        'series':series
    }
    return render(request, 'movies/index.html', context)
def detail(request):
    pass
def like(request):
    pass
def movie_detail(request):
    pass
def review_create(request):
    pass
def review_delete(request):
    pass