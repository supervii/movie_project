from django.contrib import admin
from .models import Genre, Movie, Rating

# Register your models here.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('pk', 'movieCode', 'title', 'year', 'description',
    'director', 'actors', 'grade', 'poster_path', 'youtube_url', 'rate', 'genre_id')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'score', 'movie_id', 'user_id',)
