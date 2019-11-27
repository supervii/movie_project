from django.db import models
from django.conf import settings

# Create your models here.
GENRE_CHOICES = (
    (1, '가족'), (2, '공포(호러)'), (3, '드라마'),
    (4, '멜로/로맨스'), (5, '미스터리'), (6, '사극'),
    (7, '스릴러'), (8, '액션'), (9, '어드벤처'),
    (10, '판타지'), (11, '코미디'), (12, '애니메이션'),
    (13, '범죄'), (14, '다큐멘터리'), (15, 'SF'),
    (16, '전쟁'), (17, '공연'), (18, '기타'), 
)

class Genre(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name


GRADE_CHOICES = (
    ('전체관람가', '전체관람가'), ('12세이상관람가', '12세이상관람가'),
    ('15세이상관람가', '15세이상관람가'), ('청소년관람불가', '청소년관람불가'),
)


class NowPlaying20(models.Model):
    title = models.CharField(max_length=150)
    code = models.CharField(max_length=20)
    image = models.CharField(max_length=300)


class Movie(models.Model):
    movieCode = models.IntegerField()
    title = models.CharField(max_length=150)
    year = models.IntegerField()
    release_date = models.CharField(max_length=50)
    description = models.TextField()
    genre = models.ForeignKey(Genre, choices=GENRE_CHOICES, on_delete=models.SET_NULL, null=True)
    director = models.CharField(max_length=45)
    actors = models.TextField(blank=True, null=True)
    grade = models.CharField(max_length=20,choices=GRADE_CHOICES)
    poster_path = models.CharField(max_length=200, blank=True, null=True, default='https://')
    backdrop_path = models.CharField(max_length=200, blank=True, null=True, default='https://')    
    youtube_url = models.CharField(max_length=200, blank=True, null=True, default='https://')
    rate = models.FloatField(blank=True, null=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies', blank=True)
   
    class Meta:
        ordering = ('pk',)

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


class RandYoutube(models.Model):
    code = models.CharField(max_length=20)

    class Meta:
        ordering = ('pk',)
