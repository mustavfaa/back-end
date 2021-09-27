import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(lveryil4j+*h6dg9&sm2umvmxvjw(&mnt1=vjf5at$3t0m9%-'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEBUG = False

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ekitaphana',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '6432',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'KEY_FUNCTION': 'cash_plagin.cash_key.make_key',
        'LOCATION': '/var/tmp/django_cache',
    }
}
