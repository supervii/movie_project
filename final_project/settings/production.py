from .base import *
from decouple import config

SECRET_KEY = config('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['movie-eivom.vqxyqc483b.ap-northeast-2.elasticbeanstalk.com']