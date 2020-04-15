# LastProject - Django(Movie_Recommend)

## 1. 목표

* 알고리즘을 이용한 영화추천 서비스 웹페이지 제작

## 2. 준비사항

1. (필수) Python Web Framework
   * Django 2.2.x
   * Python 3.7.x
2. (선택) 샘플 영화 정보
3. (선택) Github Flow

## 3. 요구사항

### 1. 데이터베이스 설계

### 2. Seed Data 구성

![ORM](/image/ORM.JPG)

### 3. `accounts` App

1. views.py

    ```python
    def signup(request): # 회원가입
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
    def login(request): # 로그인
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
        
    def logout(request): # 로그아웃
            auth_logout(request)
            return redirect('series:index')
        
    
        @login_required
        def detail(request, pk): # 회원정보
            detail_user = get_user_model().objects.get(pk=pk)
            context = {
                'detail_user': detail_user
            }
            return render(request, 'accounts/detail.html', context)
    
    
        
    @login_required
    def following(request, pk): # 팔로우기능
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
                    return JsonResponse({'user':user.username, 'user_pk': user.pk, 'cnt_followers': cnt_followers, 'is_follow': is_follow})
        
    
    ```

2. 결과

    * 로그인 창

      ![로그인창](/image/로그인창.JPG)
      
    * 회원가입 창
    
      ![회원가입창](/image/회원가입창.JPG)
    
    * 회원 상세보기
    
      ![프로필](/image/프로필.JPG)
    
      

### 4. `Movies` app

1. views. py

    ```python
    def index(request): # 메인 화면
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
        
    def detail(request, series_pk): # 시리즈 상세보기 화면
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
    def like(request, series_pk): # 좋아요 기능
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
    
    @login_required
    def room(request, series_pk): # 채팅방 기능
        series = get_object_or_404(Series, pk=series_pk)
        user = request.user
        return render(request, 'series/room.html', {
            'room_name_json': mark_safe(json.dumps(series_pk)),
            'user_name': mark_safe(json.dumps(user.username)),
            'series': series,
        })
        
    def search(request): # 검색 기능
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
    def comment_create_ajax(request): # 댓글작성(비동기처리)
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
    def review_delete(request): # 댓글 삭제
        review_id = int(request.POST.get('review_id'))
        review = get_object_or_404(Review, pk=review_id)
        if request.method == 'POST':
            review.delete()
        context = {
                'review_id' : review_id
            }
        return HttpResponse(json.dumps(context), content_type="application/json")
    
    @login_required
    def suggest(request): # 시리즈 추가
        suggest = Request()
        series = Series.objects.all()
        if request.method == 'POST':
            suggest.series_name = request.POST.get('name')
            suggest.user = request.user
            suggest.save()
            return redirect('series:index')
        context = {
            'series': series
        }
        return render(request, 'series/suggest.html', context)
    
    
    ```
    
2. 결과 (http://seriessy.herokuapp.com/series)

    * 메인페이지

      ![메인페이지](/image/메인페이지.JPG)

    * 메인페이지(시리즈)

      ![영화메인페이지](/image/영화메인페이지.JPG)

    * 시리즈 상세페이지

      ![시리즈상세페이지](/image/시리즈상세페이지.JPG)
    
    * 동영상 ![동영상](/image/동영상.JPG)
    
    
    

