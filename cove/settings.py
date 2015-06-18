"""
Django settings for cove project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import environ
env = environ.Env(  # set default values and casting
    SENTRY_DSN=(str, ''),
    DEBUG=(bool, True),
    PIWIK_URL=(str, ''),
    PIWIK_SITE_ID=(str, ''),
    ALLOWED_HOSTS=(list, []),
)

PIWIK = {
    'url': env('PIWIK_URL'),
    'site_id': env('PIWIK_SITE_ID'),
}


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DEALER_TYPE = 'git'

from django.utils.translation import ugettext_lazy as _
COVE_CONFIG_BY_NAMESPACE = {
    'base_template_name': {
        'cove-ocds': 'base_ocds.html',
        'cove-360': 'base_360.html',
        'default': 'base_generic.html',
    },
    'application_name': {
        'cove-ocds': _('Open Contracting Data Tool'),
        'cove-360': _('360Giving Data Tool'),
        'default': _('Cove'),
    },
    'schema_url': {  # Schema url for the package schema (does not yet exist for 360)
        'cove-ocds': 'http://localhost:8002/release-package-schema.json',
        'default': None
    },
    'item_schema_url': {  # Schema url for an individual item e.g. a single release or grant
        'cove-ocds': 'http://localhost:8002/release-schema.json',
        'cove-360': 'http://localhost:8001/360-giving-schema.json',
        'default': None
    },
    'main_sheet_name': {
        'cove-ocds': 'releases',
        'cove-360': 'grants',
        'default': None
    },
    'root_id': {
        'cove-ocds': 'ocid',
        'default': ''
    },
    'convert_titles': {
        'cove-360': True,
        'default': False
    }
}


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vank@j*7v8#%k6c-*tpsl1&z$!8qniq*@-q_&k1_^1jf5x6##n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')

RAVEN_CONFIG = {
    'dsn': env('SENTRY_DSN')
}


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'bootstrap3',
    'cove',
    'cove.input',
    'raven.contrib.django.raven_compat',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'dealer.contrib.django.Middleware',
    'cove.middleware.CoveConfigByNamespaceMiddleware',
)

ROOT_URLCONF = 'cove.urls_multi'

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
                'cove.context_processors.piwik',
                'cove.context_processors.cove_namespace_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'cove.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


LANGUAGES = (
    ('fr', 'French'),
    ('en', 'English'),
    ('es', 'Spanish'),
    ('ro', 'Romanian'),
)
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
