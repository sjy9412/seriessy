from django.shortcuts import render, get_object_or_404, redirect
from .models import Genre, Movie, Review, Series
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    series = Series.objects.all()
    context = {
        'series':series
    }
    return render(request, 'series/index.html', context)

def detail(request, series_pk):
    series = get_object_or_404(Series, pk=series_pk)
    movies = series.movie_set.all()
    context = {
        'series': series,
        'movies': movies
    }
    return render(request, 'series/detail.html', context)

def like(request, series_pk):
    if request.method == 'POST':
        series = get_object_or_404(Series, pk=series_pk)
        if request.user in series.like_users.all():
            series.like_users.remove(request.user)
        else:
            series.like_users.add(request.user)
    return redirect('series:detail', series_pk)

def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie,pk=movie_pk)
    forms = ReviewForm()
    reviews = movie.review_set.all()
    context = {
        'movie': movie, 
        'forms': forms,
        'reviews': reviews
    }
    return render(request, 'series/movie_detail.html', context)

def like_users(request, series_pk):
    series = get_object_or_404(Series, pk=series_pk)
    context = {
        'series': series
    }
    return render(request, 'series/like_users.html', context)

@login_required
def review_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        forms = ReviewForm(request.POST)
        if forms.is_valid():
            review = forms.save(commit=False)
            review.user = request.user
            review.movie = movie
            forms.save()
    return redirect('series:movie_detail', movie_pk)

@login_required
def review_delete(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
        review.delete()
    return redirect('series:movie_detail', movie_pk)

    