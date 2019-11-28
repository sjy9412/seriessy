from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    # 배포된 url
]

import django_heroku
django_heroku.settings(locals())