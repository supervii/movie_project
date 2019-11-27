from .base import *
from decouple import config
SECRET_KEY = config('SECRET_KEY', default='26+fj4km^q_+xq)d@sih07wcwt09*w*-fvmlu52w#6z2u-gue&')

DEBUG = True

ALLOWED_HOSTS = []