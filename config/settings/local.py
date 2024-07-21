from .base import *  # noqa

SECRET_KEY = "dev"

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "bookstore",
        "USER": "django",
        "PASSWORD": "django",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
