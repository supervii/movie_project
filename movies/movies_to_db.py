import csv, io
from django.shortcuts import render
from .models import Movie, Genre

# Create your views here.
def movie_upload(request):
    movies = Movie.objects.all()
    template = 'movie_upload.html'
    prompt = {
        'order': 'movieCode, title, year, description, genre, director, grade, actors, poster_path, youtube_url, rate',
        'movies': movies,
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
            description=col[3],
            genre_id=col[4],
            director=col[5],
            grade=col[6],
            actors=col[7][1:-2].replace("'", "") if col[7] else '',
            poster_path=col[8],
            youtube_url=col[9],
            rate=col[10]            
        )
    
    context = {}
    return render(request, template, context)