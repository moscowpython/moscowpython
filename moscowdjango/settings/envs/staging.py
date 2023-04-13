from __future__ import annotations

from configurations import values

from moscowdjango.settings.envs.base import Base


class Staging(Base):
    DEBUG = values.BooleanValue(False)

    SECRET_KEY = values.SecretValue()

    CSRF_TRUSTED_ORIGINS = values.ListValue(['https://dev.moscowpython.ru'])

    ALLOWED_HOSTS = values.ListValue(['dev.moscowpython.ru', '45.8.250.219'])

    AWS_ACCESS_KEY_ID = values.Value()
    AWS_SECRET_ACCESS_KEY = values.Value()
    AWS_STORAGE_BUCKET_NAME = values.Value()
    AWS_QUERYSTRING_AUTH = False

    STATIC_AWS_ACCESS_KEY_ID = values.Value()
    STATIC_AWS_SECRET_ACCESS_KEY = values.Value()
    STATIC_AWS_STORAGE_BUCKET_NAME = values.Value()

    @property
    def STATIC_URL(self):
        return f'https://{self.STATIC_AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/'

    STORAGES = {
        'default': {'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage', 'OPTIONS': {'location': 'media'}},
        'staticfiles': {'BACKEND': 'moscowdjango.storage_backends.S3StaticStorage'},
    }
