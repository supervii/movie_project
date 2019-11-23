from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django views.decorators.http import require_POST
from .models import Movie, Genre, Rating
from .forms import RatingFrom

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    context = {'movies': movies,}
    return render(request, 'movies/index.html', context)


def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)