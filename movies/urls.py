from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/delete/', views.delete, name='delete'),
    path('<int:movie_pk>/update/', views.update, name='update'),
    path('<int:movie_pk>/ratings/', views.rating_create, name='rating_create'),
    path('<int:movie_pk>/ratings/<int:rating_pk>/delete/', views.rating_delete, name='rating_delete'),
    path('<int:movie_pk>/like/', views.like, name='like'),
]
