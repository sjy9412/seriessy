from django.shortcuts import render, get_object_or_404, redirect
from .models import Genre, Movie, Review, Series


# Create your views here.

def index(request):
    series = Series.objects.all()
    context = {
        'series':series
    }
    return render(request, 'movies/index.html', context)

def detail(request, series_pk):
    series = get_object_or_404(Series, pk=series_pk)
    movies = series.movie_set.all()
    context = {
        'series': series,
        'movies': movies
    }
    return render(request, 'movies/detail.html', context)

def like(request):
    if request.method == 'POST':
        series = get_object_or_404(Series, pk=movie_pk)
        if request.user in series.like_users.all():
            series.like_users.remove(request.user)
        else:
            series.like_users.add(request.user)
    return redirect('movies:detail', series_pk)

def movie_detail(request, series_pk, movie_pk):
    movie = get_object_or_404(Movie,pk=movie_pk)
    context = {
        'movie':movie
    }
    return render(request, 'movies/movie_detail.html', context)

def review_create(request):
    pass
def review_delete(request):
    pass