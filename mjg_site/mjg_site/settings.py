"""
Django settings for mjg_site project.

Generated by 'django-admin startproject' using Django 1.11.16.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f8t_-f!filk*vhx3+&9@%+4!8g%enw(+*^#h96%#di%t9j8t3i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'website',
    'account_app',
    'mkauto_app',
    'email_app',
    'anymail',
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

ROOT_URLCONF = 'mjg_site.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'mjg_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'it-IT'
LOCALE = 'it_IT.utf8'

TIME_ZONE = 'Europe/Rome'

USE_I18N = True

USE_L10N = True

USE_TZ = True

"""
HOW TO SUL TIMEZONE

SE UTILIZZO USE_TZ = True
Le date sono memorizzate con UTC, va utilizzata la funzione timezone.now() per ottenere la data in UTC,
per poterla visualizzare con il timezone settato di default (TIME_ZONE) utilizzare la funzione timezone.localtime(timezone.now())
Postgres di default salva le date in formato UTC, mysql no, in questo caso settare nella configurazione del db
il timezone da utilizzare:
https://docs.djangoproject.com/en/1.11/topics/i18n/timezones/#setup

Alcune funzioni di esempio:
logger.info("datetime.datetime.today(): " + str(datetime.datetime.today()))
logger.info("datetime.datetime.now(): " + str(datetime.datetime.now()))
logger.info("timezone.now(): " + str(timezone.now()))
logger.info("datetime.timedelta(days=30): " + str(datetime.timedelta(hours=1)))
logger.info("timezone.localtime(timezone.now()): " + str(timezone.localtime(timezone.now())))
logger.info("timezone.now()-datetime.timedelta(hours=1): " + str(timezone.now()-datetime.timedelta(hours=1)))
logger.info("timezone.now()-datetime.timedelta(hours=1): " + str(timezone.now()-datetime.timedelta(days=days_from_creation)))
"""

LOGIN_URL = "/admin/login/"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
GIT_PROJECT_NAME = "mjg"

# loading local settings
try:
    LOCAL_SETTINGS
except NameError:
    try:
        from local_settings import *
    except ImportError:
        pass
