"""
Django settings for reservas project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'llu^8q(j^m3i1g$w=nmo4it0q4jresbchc(2#skb^d*02bbcgl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'formtools',
    'crispy_forms',
    'reservas',
    'descuentos',
    'encuesta',
    'retiros',
    'lacalma',
    'raven.contrib.django.raven_compat',
    'django_nose',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'reservas.urls'

WSGI_APPLICATION = 'reservas.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Argentina/Cordoba'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 3


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

MP_CLIENT_ID = ''       # set it in your local_settings.py
MP_CLIENT_SECRET = ''
MP_SANDBOX_MODE = True


RAVEN_CONFIG = {
    'dsn': 'https://:8cf565593e7e42a38a3332b567601034@app.getsentry.com/34941',
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['-s', '--nologcapture', '--nocapture', '--with-id',
             '--logging-clear-handlers']


EMAIL_ADMIN_RETIROS = 'gaitan@gmail.com'

try:
    from .local_settings import *
except:
    pass