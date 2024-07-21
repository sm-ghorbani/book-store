from .base import *  # noqa

SECRET_KEY = "dev"

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "book",
        "USER": "book",
        "PASSWORD": "django",
        "HOST": "localhost",
        "PORT": "",
    }
}
