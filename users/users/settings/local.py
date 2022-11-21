from .base import *
import psycopg2

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dbuser',
        "USER": "dbadmin",
        "PASSWORD": "DB2022",
        #'NAME':get_secret('DB_NAME'),
        #'USER':get_secret('USER'),
        #'PASSWORD': get_secret('PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',

    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS =[BASE_DIR.parent /'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.parent / 'media'

#EMAIL SETTING
EMAIL_USE_TLS= True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = get_secret('EMAIL')
EMAIL_HOST_PASSWORD = get_secret('PASS_EMAIL')
EMIAL_PORT= 587