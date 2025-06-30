from .base import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'django', 'backend']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pdfdb',
        'USER': 'pdfuser',
        'PASSWORD': 'pdfpass',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
