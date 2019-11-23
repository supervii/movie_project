from django import forms
from .models import Movie, Genre, Rating


class MovieForm(forms.ModelForm):
    movieCode = forms.IntegerField()
    title = forms.CharField(
        label='영화제목',
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'movie-title',
                'placeholder': '영화제목을 입력하세요.',
            }
        )
    )
    year = forms.IntegerField()
    description = forms.CharField(
        label='영화 줄거리',
        widget=forms.Textarea(
            attrs={
                'class': 'movie-description',
                'placeholder': '영화 줄거리를 입력하세요.',
                'rows': 5,
                'cols': 50,
            }
        )
    )
    genre = forms.ModelMultipleChoiceField(queryset=Genre.objects.all())
    director = forms.CharField(
        label='감독',
        max_length=45,
        widget=forms.TextInput(
            attrs={
                'class': 'movie-director',
                'placeholder': '감독명을 입력하세요.',
            }
        )
    )
    grade = forms.CharField(
        label='영화관람등급',
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'movie-grade',
                'placeholder': '관람등급을 입력하세요. (예: "전체관람가", "12세이상관람가" 등 띄어쓰기 없이)',
            }
        )
    )
    actors = forms.CharField(
        label='영화출연배우',
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'movie-actors',
                'placeholder': '출연 배우 이름을 입력하세요.',
            }
        )
    )
    poster_path = forms.CharField(
        label='영화 이미지 URL',
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'movie-poster',
                'placeholder': '포스터 이미지 주소를 입력하세요.',
            }
        )
    )
    youtube_url = forms.CharField(
        label='Youtube URL',
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'movie-youtube',
                'placeholder': '유튜브 주소를 입력하세요.',
            }
        )
    )
    rate = forms.FloatField(max_value=10.0, min_value=0.0)

    class Meta:
        model = Movie
        fields = ('movieCode', 'title', 'year', 'description', 'genre',
        'director', 'grade', 'actors', 'poster_path', 'youtube_url', 'rate',)


class RatingForm(forms.ModelForm):
    comment = forms.CharField(
        label='리뷰',
        widget=forms.Textarea(
            attrs={
                'class': 'rating-comment',
                'placeholder': '리뷰를 작성하세요',
            }
        )
    )
        
    score = forms.IntegerField(max_value=10, min_value=0)

    class Meta:
        model = Rating
        fields = ('comment', 'score',)