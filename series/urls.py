from django.urls import path
from . import views

app_name = 'series'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:series_pk>/movie/<int:movie_pk>/', views.detail, name="detail"),
    path('<int:series_pk>/room/', views.room, name='room'),
    path('<int:series_pk>/like/', views.like, name="like"),
    path('<int:movie_pk>/movie/', views.movie_detail, name="movie_detail"),
    # path('<int:series_pk>/movie/<int:movie_pk>/reviews/create/', views.review_create, name="review_create"),
    path('<int:movie_pk>/movie/reviews/<int:review_pk>/delete/', views.review_delete, name="review_delete"),
    path('search/', views.search, name='search'),
    path('comment/create/', views.comment_create_ajax, name='comment_create_ajax'),
]
