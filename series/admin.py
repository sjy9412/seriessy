from django.contrib import admin
from .models import Genre, Movie, Series, Review, Score, Request

# Register your models here.

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Series)
admin.site.register(Review)
admin.site.register(Score)
admin.site.register(Request)

