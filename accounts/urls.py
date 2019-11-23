from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    #  관리자 Path
    path('', views.main, name='main'),
    path('users/', views.list, name='list'),
    #  유저 Path
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:user_pk>/', views.detail, name='detail'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
]
