from django.contrib import admin
from .models import Genre, NowPlaying20, Movie, Rating, RandYoutube

# Register your models here.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)


@admin.register(NowPlaying20)
class NowPlaying20Admin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'code', 'image',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('pk', 'movieCode', 'title', 'year', 'release_date', 'description',
    'director', 'actors', 'grade', 'poster_path', 'backdrop_path', 'youtube_url', 'rate', 'genre_id')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'score', 'movie_id', 'user_id',)


@admin.register(RandYoutube)
class RandYoutubeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'code',)
