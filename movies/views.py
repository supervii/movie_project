from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .models import Movie, Rating
from .forms import MovieForm, RatingForm

# Create your views here.
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
        else:
            return redirect('movies:index')
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
