"""
Django settings for nothotdog project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'uqeie!xzul-n#l366htzipauu1awzo&m)crjbu)sa*4#l=2%&6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

ADMINS = [
    ('Jesper', 'jesper@trell.se'),
]

SERVER_EMAIL = 'info@trell.se'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    'nothotdog',
    'nothotdog.photos',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nothotdog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'nothotdog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'photos',
        'USER': 'postgres',
        'PASSWORD': 'admin1',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Stockholm'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
    os.path.join(BASE_DIR, 'node_modules'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

COMPRESS_OFFLINE = False

COMPRESS_OUTPUT_DIR = ''

try:
    from nothotdog.local_settings import *  # noqa
except ImportError:
    pass

NODE_ENV = 'development' if DEBUG else 'production'

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'node_modules/.bin/node-sass {infile} {outfile}'),
    ('text/jsx', 'NODE_ENV={} node_modules/.bin/browserifyinc '
                 '--debug '
                 '-t babelify {{infile}} -o {{outfile}}'.format(NODE_ENV)),
)

if not DEBUG:
    COMPRESS_OFFLINE = True
    COMPRESS_PRECOMPILERS = (
        ('text/x-scss', 'node_modules/.bin/node-sass {infile} {outfile}'),
        ('text/jsx', 'NODE_ENV=production node_modules/.bin/browserify '
            '-t babelify {infile} -o {outfile}'),
    )

LOGIN_REDIRECT_URL = 'photos:index'
LOGOUT_REDIRECT_URL = 'photos:index'

RABBITMQ_HOST = 'localhost'

ML_DATA_PATH = str(BASE_DIR) + '/hotdog_finder/hotdog_data'
ML_MODEL_PATH = str(BASE_DIR) + '/hotdog_finder/hotdog_CNN_model'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ]
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{asctime} - {name} - {levelname} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'events.log',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'nothotdog.photos.management.commands.uploadlistener': {
            'level': 'INFO',
            'handlers': ['file'],
        },
    },
}
