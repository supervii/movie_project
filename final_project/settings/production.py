from .base import *
from decouple import config

SECRET_KEY = config('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['eivom-movie.cmxvdvr7qt.ap-northeast-2.elasticbeanstalk.com']