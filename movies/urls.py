from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:series_pk>/', views.detail, name="series_detail"),
    path('<int:series_pk>/like', views.like, name="like"),
    path('<int:series_pk>/movies/<int:movie_pk>/', views.movie_detail, name="movie_detail"),
    path('<int:series_pk>/movies/<int:movie_pk>/reviews/<int:review_pk>/create/', views.review_create, name="review_create"),
    path('<int:series_pk>/movies/<int:movie_pk>/reviews/<int:review_pk>/delete/', views.review_delete, name="review_delete"),
]
