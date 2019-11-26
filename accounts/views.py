from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationFrom
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup(request):
    if request.method == 'POST':
        forms = CustomUserCreationFrom(request.POST)
        if forms.is_valid():
            user = forms.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('series:index')
    else:
        forms = CustomUserCreationFrom()
    context = {
        'forms': forms
    }
    return render(request, 'accounts/form.html', context)

def login(request):
    if request.method == 'POST':
        forms = AuthenticationForm(request, request.POST)
        if forms.is_valid():
            user = forms.get_user()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(request.GET.get('next') or 'series:index')
    else:
        forms = AuthenticationForm()
    context = {
        'forms': forms
    }
    return render(request, 'accounts/form.html', context)

def logout(request):
    auth_logout(request)
    return redirect('series:index')

@login_required
def detail(request, pk):
    detail_user = get_user_model().objects.get(pk=pk)
    context = {
        'detail_user': detail_user
    }
    return render(request, 'accounts/detail.html', context)


@login_required
def following(request, pk):
    if request.is_ajax():
        detail_user = get_user_model().objects.get(pk=pk)
        user = request.user
        if detail_user != request.user:
            if request.user in detail_user.followers.all():
                detail_user.followers.remove(user)
                is_follow = True
            else:
                detail_user.followers.add(user)
                is_follow = False
            cnt_following = detail_user.followings.count()
            cnt_followers = detail_user.followers.count()
            return JsonResponse({'cnt_following': cnt_following, 'cnt_followers': cnt_followers, 'is_follow': is_follow})

