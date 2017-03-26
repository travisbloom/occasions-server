"""
Django settings for occasions project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import raven
import sys
import logging

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['OCCASIONS_DJANGO_SECRET_KEY']
STRIPE_SECRET_KEY = os.environ['OCCASIONS_STRIPE_SECRET_KEY']
STRIPE_TEST_USER_ID = os.environ['OCCASIONS_STRIPE_TEST_USER_ID']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('OCCASIONS_ENVIRONMENT') == 'local'
ALLOWED_HOSTS = []
TESTING = sys.argv[1:2] == ['test']

if TESTING:
    logging.disable(logging.CRITICAL)

# Application definition

INSTALLED_APPS = [
    'people.apps.PeopleConfig',
    'events.apps.EventsConfig',
    'locations.apps.LocationsConfig',
    'products.apps.ProductsConfig',
    'transactions.apps.TransactionsConfig',

    'django_extensions',
    'django_graphiql',
    'graphene_django',

    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',
    'corsheaders',

    'django_filters',

    'raven.contrib.django.raven_compat',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'debug_toolbar',
    'debug_panel'
]


MIDDLEWARE = [
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'debug_panel.middleware.DebugPanelMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'common.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'common.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

# graphql

GRAPHENE_SCHEMA = 'common.schema'
GRAPHENE_SCHEMA_OUTPUT = 'assets/schema.json'
GRAPHENE_SCHEMA_INDENT = 4

# auth
AUTH_USER_MODEL = 'people.User'
CORS_ORIGIN_ALLOW_ALL = True

AUTHENTICATION_BACKENDS = (
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

INTERNAL_IPS = (
    '127.0.0.1'
)


# logging
RAVEN_CONFIG = {
    'dsn': None if DEBUG else os.environ['OCCASIONS_SENTRY_DNS'],
    'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            # To capture more than ERROR, change to WARNING, INFO, etc.
            'level': 'CRITICAL' if DEBUG else 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'django': {
            'level': 'DEBUG',
            'handlers': ['console', 'sentry'],
            'propagate': True,
        },
        'raven': {
            'level': 'INFO',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'INFO',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'occasions': {
            'level': 'DEBUG',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        }
    },
}
