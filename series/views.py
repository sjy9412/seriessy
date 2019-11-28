from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Genre, Movie, Review, Series, Score, Request
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json, random
from IPython import embed
def result(series_all, user):
    my_genre = set()
    for my in user.like_series.all():
        for g in my.genre.all():
            my_genre.add(g.name)
    for s in series_all:
        if Score.objects.filter(user_id=user).filter(series_id=s.pk):
            newscore = Score.objects.filter(user_id=user).filter(series_id=s.pk)[0]
        else:
            newscore = Score()
        score = 0
        newscore.user = user
        for g in s.genre.all():
            cnt = 0
            if g.name in my_genre:
                cnt += 1
        if 0 < cnt < 3:
            score += 2
        elif 2 <= cnt:
            score += 3
        for follower in user.followings.all():
            for review in follower.review_set.all():
                if review.series_id == s.pk:
                    if review.score <= 1:
                        score -= 2
                    elif 1 < review.score <= 2:
                        score -= 1
                    elif 3 < review.score <= 4:
                        score += 1
                    elif 4 < review.score <= 5:
                        score += 2
            for series in follower.like_series.all():
                if series.pk == s.pk:
                    score += 2
        newscore.series = s
        newscore.user_score = score
        newscore.save()
    return user.score_series.order_by('-score__user_score')
# Create your views here.
def index(request):
    series = Series.objects.all()
    user = request.user
    if user.is_authenticated:
        series = result(series, user)
    else:
        series = list(series)
        random.shuffle(series)
    context = {
        'series':series,
    }
    return render(request, 'series/index.html', context)
def detail(request, series_pk):
    series = get_object_or_404(Series, pk=series_pk)
    movie_pk = request.GET.get('movie_pk')
    forms = ReviewForm()
    context = {
        'series': series,
        'movie_pk': int(movie_pk),
        'forms': forms,
        'room_name_json': mark_safe(json.dumps(series_pk)),
        'user_name': mark_safe(json.dumps(request.user.username)),
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
        'reviews': reviews,
    }
    return render(request, 'series/movie_detail.html', context)
# @login_required
# def review_create(request, series_pk, movie_pk):
#     series = get_object_or_404(Series, pk=series_pk)
#     reviews = series.review_set.all()
#     if request.method == 'POST':
#         for review in reviews:
#             if request.user == review.user:
#                 forms = ReviewForm(request.POST, instance=review)
#                 forms.save()
#                 break
#         else:
#             forms = ReviewForm(request.POST)
#             if forms.is_valid():
#                 review = forms.save(commit=False)
#                 review.user = request.user
#                 review.series = series
#                 forms.save()
#     return redirect('series:detail', series_pk, movie_pk)
@login_required
def review_delete(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
        review.delete()
    return redirect('series:movie_detail', movie_pk)
@login_required
def room(request, series_pk):
    series = get_object_or_404(Series, pk=series_pk)
    user = request.user
    return render(request, 'series/room.html', {
        'room_name_json': mark_safe(json.dumps(series_pk)),
        'user_name': mark_safe(json.dumps(user.username)),
        'series': series,
    })
def search(request):
    series = Series.objects.all()
    search = request.GET.get('search')
    if search != '':
        for s in series:
            name = s.name.replace(' ', '')
            if search in name or search in s.name:
                return redirect(f'/series/#{s.pk}')
    user = request.user
    if user.is_authenticated:
        series = result(series, user)
    else:
        series = list(series)
        random.shuffle(series)
    context = {
        'series':series,
    }
    return render(request, 'series/index.html', context)
@login_required
def comment_create_ajax(request):
    series = get_object_or_404(Series, pk=int(request.POST.get('series_id')))
    reviews = series.review_set.all()
    for review in reviews:
        if request.user == review.user:
            review.content = request.POST.get('content')
            review.score = int(request.POST.get('score'))
            review.save()
            chk = False
            break
    else:
        review = Review()
        review.content = request.POST.get('content')
        review.series = get_object_or_404(Series, pk=int(request.POST.get('series_id')))
        review.user = request.user
        review.score = int(request.POST.get('score'))
        review.save()
        chk = True
    context = {
        'content' : review.content,
        'score' : review.score,
        'username' : request.user.username,
        'review_id' : review.pk,
        'chk' : chk
    }
    return HttpResponse(json.dumps(context), content_type="application/json")
@login_required
def review_delete(request):
    review_id = int(request.POST.get('review_id'))
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'POST':
        review.delete()
    context = {
            'review_id' : review_id
        }
    return HttpResponse(json.dumps(context), content_type="application/json")

def suggest(request):
    suggest = Request()
    series = Series.objects.all()
    if request.method == 'POST':
        suggest.series_name = request.POST.get('name')
        suggest.user = request.user
        suggest.save()
        return redirect('series:suggest')
    context = {
        'series': series
    }
    return render(request, 'series/suggest.html', context)
