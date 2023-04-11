from __future__ import annotations

from configurations import values

from moscowdjango.settings.envs.base import Base


class Dev(Base):
    ALLOWED_HOSTS = ['*']  # noqa: allowed straight assignment
    DEBUG = True  # noqa: allowed straight assignment

    AWS_ACCESS_KEY_ID = values.Value()
    AWS_SECRET_ACCESS_KEY = values.Value()
    AWS_STORAGE_BUCKET_NAME = values.Value()
    AWS_QUERYSTRING_AUTH = False

    STORAGES = {
        'default': {'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage', 'OPTIONS': {'location': 'media'}},
        'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
    }
