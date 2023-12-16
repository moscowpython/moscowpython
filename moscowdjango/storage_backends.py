from __future__ import annotations

from django.conf import settings

from storages.backends.s3boto3 import S3StaticStorage as S3StaticStorageBase


class S3StaticStorage(S3StaticStorageBase):
    access_key = settings.STATIC_AWS_ACCESS_KEY_ID
    secret_key = settings.STATIC_AWS_SECRET_ACCESS_KEY
    bucket_name = settings.STATIC_AWS_STORAGE_BUCKET_NAME
    location = 'static'
