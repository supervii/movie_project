from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .models import NowPlaying20, Movie, Rating, RandYoutube
from .forms import MovieForm, RatingForm

import requests
import csv, io
from bs4 import BeautifulSoup


# Create your views here.
def now_playing(request):
    nowplays = NowPlaying20.objects.all()
    utubes = RandYoutube.objects.all()
    context = {'nowplays': nowplays, 'utubes': utubes,}
    return render(request, 'movies/main.html', context)


def index(request):
    movies = Movie.objects.all()
    context = {'movies': movies, }
    return render(request, 'movies/index.html', context)


def main(request):
    movies = Movie.objects.all()
    context = {'movies': movies, }
    return render(request, 'movies/main.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = MovieForm(request.POST)
            if form.is_valid():
                form.save()
        else:
            form = MovieForm()
        context = {'form': form,}
        return render(request, 'movies/form.html', context)
    else:
        return HttpResponse('관리자만 접근 가능합니다.')


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.user.is_superuser:
        if request.method == 'POST':
            form = MovieForm(request.POST, instance=movie)
            if form.is_valid():
                form.save()
                return redirect('movies:detail', movie_pk)
        else:
            form = MovieForm(instance=movie)
        # 1. POST 방식일 때 오는 FORM: 검증에 실패한 form - 오류메시지도 포함된 상태
        # 2. GET 방식일 때 오는 FORM: 초기화된 form
        context = {'form': form, 'movie': movie,}
        return render(request, 'movies/form.html', context)
    else:
        return HttpResponse('관리자만 접근 가능합니다.')


def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    ratings = movie.rating_set.all()
    rating_form = RatingForm()
    context = {
        'movie': movie,
        'ratings': ratings,
        'rating_form': rating_form,
    }
    return render(request, 'movies/detail.html', context)


@login_required
@require_POST
def delete(request, movie_pk):
    if request.user.is_superuser:
        movie = get_object_or_404(Movie, pk=movie_pk)
        movie.delete()
        return redirect('movies:index')
    else:
        return HttpResponse('관리자만 접근 가능합니다.')


@require_POST
def rating_create(request, movie_pk):
    if request.user.is_authenticated:
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.movie_id = movie_pk
            rating.user = request.user
            rating.save()
    return redirect('movies:detail', movie_pk)


@require_POST
def rating_delete(request, movie_pk, rating_pk):
    if request.user.is_authenticated:
        rating = get_object_or_404(Rating, pk=rating_pk)
        if request.user == rating.user:
            rating.delete()
        return redirect('movies:detail', movie_pk)

@login_required
def rating_update(request, rating_pk, movie_pk):
    rating = get_object_or_404(Rating, pk=rating_pk)
    if request.user == rating.user:
        if request.method == 'POST':
            form = RatingForm(request.POST, instance=rating)
            if form.is_valid():
                form.save()
                return redirect('movies:detail', movie_pk)
        else:
            form = RatingForm(instance=rating)
        context = {
            'form': form,
        }
        return render(request, 'movies/form.html', context)
    else:
        return redirect('movies:detail', movie_pk)


@login_required
def like(request, movie_pk):
    if request.is_ajax():
        movie = get_object_or_404(Movie, pk=movie_pk)
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)
            liked = False
        else:
            movie.like_users.add(request.user)
            liked = True
        context = {'liked': liked, 'count': movie.like_users.count(),}
        return JsonResponse(context)
    else:
        return HttpResponseBadRequest()


def find_movie(request):
    query = request.GET.get('search_title')
    if query:
        title_movies = Movie.objects.filter(title__icontains=query)
        filtered_movies = Movie.objects.filter(description__icontains=query)
        d_movies = filtered_movies - title_movies
        context = {
            "title_movies" : title_movies,
            "d_movies" : d_movies
        }
        return render(request,'movies/search.html',context)
    else:
        return redirect('movies:index', 0)


def search(request):
    movies = Movie.objects.all()
    users = User.objects.all()
    genres = Genre.objects.all()
    movies_list = []
    users_list = []
    genres_list = []
    g_pk = 0
    search = request.GET.get("search")
    print(search)
    for genre in genres:
        if search in genre.name:
            g_pk = genre.pk
            break
    for movie in movies:
        if search in movie.title:
            movies_list.append(movie)
        if movie.genres.all().filter(pk=g_pk):
            genres_list.append(movie)
    for user in users:
        if search in user.username:
            users_list.append(user)
    context = {
        "movies" : movies_list,
        "users" : users_list,
        "genres" : genres_list 
    }
    # print("들어왔당")
    return render(request, 'movies/search.html', context)


# 아래부터는 DB에 넣을 것
def get_movie_upload(request):
    movies = Movie.objects.all()
    nowplays = NowPlaying20.objects.all()
    template = 'movie_upload.html'
    prompt = {
        'order': 'movieCode, title, year, release_date, description, genre, director, grade, actors, poster_path, backdrop_path, youtube_url, rate',
        'movies': movies,
        # 'nowplays': nowplays,
    }
    if request.method == 'GET':
        return render(request, template, prompt)
    
    csv_file = request.FILES['file']

    data_set = csv_file.read().decode('UTF-8')

    io_string = io.StringIO(data_set)
    next(io_string)
    # print(data_set)
    for col in csv.reader(io_string):
        _, created = Movie.objects.update_or_create(
            movieCode=col[0],
            title=col[1],
            year=col[2],
            release_date=col[3],
            description=col[4],
            genre_id=col[5],
            director=col[6],
            grade=col[7],
            actors=col[8][1:-2].replace("'", "") if col[8] else '',
            poster_path=col[9],
            backdrop_path=col[10],
            youtube_url=col[11],
            rate=col[12]
        )
    
    context = {}
    return render(request, template, context)


def get_nowplaying(request):
    nowplays = NowPlaying20.objects.all()
    # utubes = RandYoutube.objects.all()
    template = 'movie_upload.html'
    # prompt = {
    #     'order': 'np_title, code',
    #     'movies': nowplays,
    # }
    # prompt = {
    #     'order': 'movieCode, title, year, release_date, description, genre, director, grade, actors, poster_path, backdrop_path, youtube_url, rate',
    #     'movies': nowplays,
    # }
    # prompt = {
    #     'order': 'you_code',
    #     'movies': utubes,
    # }
    if request.method == 'GET':
        return render(request, template, prompt)
    
    csv_file = request.FILES['file']

    data_set = csv_file.read().decode('UTF-8')

    io_string = io.StringIO(data_set)
    next(io_string)
    # for col in csv.reader(io_string):
    #     _, created = NowPlaying20.objects.update_or_create(
    #         title=col[0],
    #         code=col[1],
    #     )
    # for col in csv.reader(io_string):
    #     for e in nowplays:
    #         if e.title == col[1]:
    #             print(e.title)
    #             created = NowPlaying20.objects.filter(pk=e.id).update(image=col[10])
    #             print(e.image)
    # for col in csv.reader(io_string):
    #     _, created = RandYoutube.objects.update_or_create(
    #         code=col[0],
    #     )
        
            
    context = {}
    return render(request, template, context)
