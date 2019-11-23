from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from movies.models import Genre

# Create your models here.
class User(AbstractUser):
    follower = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings')

class Profile(models.Model):
    user            = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    nickname        = models.CharField(max_length = 30)
    introduction    = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
