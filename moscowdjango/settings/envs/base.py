from __future__ import annotations

import os

import sentry_sdk
from configurations import Configuration, values
from sentry_sdk.integrations.django import DjangoIntegration


class Base(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    SECRET_KEY = values.Value('1951f79c-537c-40be-9847-992bc735261a')

    DEBUG = True  # noqa: allowed straight assignment

    SITE_ID = 1

    ALLOWED_HOSTS = ['*']  # noqa: allowed straight assignment

    AUTH_USER_MODEL = 'auth.User'  # noqa: allowed straight assignment

    DEFAULT_AUTO_FIELD = "django.db.models.AutoField"  # noqa: allowed straight assignment

    INSTALLED_APPS = [  # noqa: static object
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'pytils',
        'apps.meetup',
    ]

    MIDDLEWARE = [  # noqa: static object
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = values.Value('moscowdjango.urls')

    TEMPLATES = [  # noqa: static object
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.messages.context_processors.messages',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'apps.meetup.context.menu',
                    'apps.meetup.context.all_events_processor',
                    'apps.meetup.context.executives',
                ]
            },
        }
    ]

    WSGI_APPLICATION = 'moscowdjango.wsgi.application'  # noqa: allowed straight assignment

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',  # noqa: allowed straight assignment
            'NAME': values.Value('moscowdjango', environ_name='DB_NAME'),
            'USER': values.Value('moscowdjango', environ_name='DB_USER'),
            'PASSWORD': values.Value('password', environ_name='DB_PASSWORD'),
            'HOST': values.Value('localhost', environ_name='DB_HOST'),
            'PORT': values.Value('5432', environ_name='DB_PORT'),
        }
    }

    AUTH_PASSWORD_VALIDATORS = [  # noqa: static object
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
        {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
        {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
        {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    ]

    LANGUAGE_CODE = 'ru-ru'  # noqa: allowed straight assignment

    TIME_ZONE = 'Europe/Moscow'  # noqa: allowed straight assignment

    USE_I18N = True  # noqa: allowed straight assignment

    USE_TZ = False  # noqa: allowed straight assignment

    STATIC_URL = values.Value('/static/')

    STATIC_ROOT = values.Value(os.path.join(BASE_DIR, 'static'))

    STATICFILES_DIRS = [  # noqa: static object
        os.path.join(BASE_DIR, 'moscowdjango', 'static'),
    ]

    MEDIA_ROOT = values.Value(os.path.join(BASE_DIR, 'media'))

    MEDIA_URL = values.Value('/media/')

    EMBEDLY_KEY = os.environ.get('EMBEDLY_KEY')

    EMBED_VIDEO_WIDTH = values.Value(854)
    EMBED_VIDEO_HEIGHT = values.Value(480)

    @property
    def SENTRY_CONFIG(self):
        self._SENTRY_CONFIG = {
            'dsn': values.Value('', environ_name='SENTRY_DSN'),
            'release': '',  # noqa: allowed straight assignment
            'integrations': [DjangoIntegration()],  # noqa: allowed straight assignment
            'environment': values.Value('', environ_name='CONFIGURATION').lower(),
            'traces_sample_rate': 1.0,  # noqa: allowed straight assignment
            'send_default_pii': True,  # noqa: allowed straight assignment
        }
        sentry_sdk.init(**self._SENTRY_CONFIG)

        return self._SENTRY_CONFIG

    @property
    def SENTRY_ENABLED(self):
        return self.SENTRY_CONFIG and self.SENTRY_CONFIG.get('dsn')
