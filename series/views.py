from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Genre, Movie, Review, Series
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json

# Create your views here.

def index(request):
    series = Series.objects.all()
    context = {
        'series':series,
        'chk': False
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

@login_required
def like(request, series_pk):
    if request.is_ajax():
        series = get_object_or_404(Series, pk=series_pk)
        user = request.user
        if user in series.like_users.all():
            series.like_users.remove(user)
            is_liked = True
        elif user.like_series.count() > 5:
            is_liked = 'max'
        else:
            series.like_users.add(user)
            is_liked = False
        count =  series.like_users.count()
        return JsonResponse({'count': count, 'is_liked': is_liked, 'user': user.username, 'pk': series_pk})
    else:
        return HttpResponseForbidden()

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


def room(request, series_pk):
    user = request.user
    return render(request, 'series/room.html', {
        'room_name_json': mark_safe(json.dumps(series_pk)),
        'user' : user.username
        
    })

def search(request):
    series = Series.objects.all()
    search = request.GET.get('search')
    if search != '':
        for s in series:
            name = s.name.replace(' ', '')
            if search in name or search in s.name:
                return redirect(f'/series/#{s.pk}')
    context = {
        'series':series,
        'chk': False
    }
    return render(request, 'series/index.html', context)
