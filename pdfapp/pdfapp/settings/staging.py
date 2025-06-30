from .base import *

DEBUG = False
ALLOWED_HOSTS = ['localhost', 'nginx', 'backend']

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'db'),
        'USER': os.getenv('POSTGRES_USER', 'user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'pass'),
        'HOST': 'postgres',
        'PORT': os.getenv('POSTGRES_PORT', 5432),
    }
}
