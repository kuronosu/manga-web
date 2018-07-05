"""
Django settings for MangaWeb project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
   from MangaWeb.environment_variables import *
except:
    print('Crear variables de entorno')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
try:
    SECRET_KEY = os.environ['SECRET_KEY']
except Exception:
    # Poner la SECRET_KEY en el archivo de configuracion local o en el entorno virtual
    pass

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
    'manageManga.apps.ManagemangaConfig',
    'accounts.apps.AccountsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'MangaWeb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
            ],
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

WSGI_APPLICATION = 'MangaWeb.wsgi.application'
AUTHENTICATION_BACKENDS = ['django-dual-authentication.backends.DualAuthentication']


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DBNAME'],
        'USER': os.environ['DBUSER'],
        'PASSWORD': os.environ['DBPASS'] ,
        'HOST': 'localhost',
        'PORT': '',                      # Set to empty string for default.
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

LANGUAGE_CODE = 'en-us'

_ = lambda s: s

LANGUAGES = (
    ('es', _('Spanish')),
    ('en', _('English')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# import dj_database_url
# db_from_env = dj_database_url.config(conn_max_age=500)
# DATABASES['default'].update(db_from_env)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

#STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

MEDIA_ROOT = 'media'

MEDIA_URL = '/media/'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = int(os.environ['EMAIL_PORT'])
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

LOGIN_REDIRECT_URL = reverse_lazy('home')
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_CASE_SENSITIVE = 'both'

try:
   from MangaWeb.local_settings import *
except Exception as e:
    pass

try:
   from MangaWeb.deploy_settings import *
except Exception as e:
    pass