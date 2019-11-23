from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name



class Movie(models.Model):
    movieCode = models.IntegerField()
    title = models.CharField(max_length=150)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    director = models.CharField(max_length=45)
    actors = models.TextField(blank=True, null=True)
    grade = models.CharField(max_length=20)
    poster_path = models.CharField(max_length=200, blank=True, null=True, default='https://')
    youtube_url = models.CharField(max_length=200, blank=True, null=True, default='https://')
    rate = models.FloatField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies', blank=True)
   
    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.title

        

class Rating(models.Model):
    comment = models.TextField()
    score = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return f'({self.user}|{self.movie}) {self.comment}'
