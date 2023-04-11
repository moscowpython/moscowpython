from __future__ import annotations

from configurations import values

from moscowdjango.settings.envs.base import Base


class Staging(Base):
    DEBUG = values.BooleanValue(False)

    SECRET_KEY = values.SecretValue()

    CSRF_TRUSTED_ORIGINS = values.ListValue(['https://dev.moscowpython.ru'])

    ALLOWED_HOSTS = values.ListValue(['dev.moscowpython.ru'])

    AWS_ACCESS_KEY_ID = values.Value()
    AWS_SECRET_ACCESS_KEY = values.Value()
    AWS_STORAGE_BUCKET_NAME = values.Value()
    AWS_QUERYSTRING_AUTH = False

    STORAGES = {
        'default': {'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage', 'OPTIONS': {'location': 'media'}},
        'staticfiles': {
            'BACKEND': 'storages.backends.s3boto3.S3ManifestStaticStorage',
            'OPTIONS': {'location': 'static'},
        },
    }
