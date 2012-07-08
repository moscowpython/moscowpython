# Django settings for moscowdjango project.
from settings import *

DEBUG = False

# Amazon credentials
AWS_ACCESS_KEY_ID = 'AKIAJVOIXG4RWCO2UFCQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'moscowdjango'
AWS_QUERYSTRING_AUTH = False

# Media & static
DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
DEFAULT_S3_PATH = "media"
STATIC_S3_PATH = "static"
MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
MEDIA_URL = 'https://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
STATIC_ROOT = "/%s/" % STATIC_S3_PATH
STATIC_URL = 'https://%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME

# Django compressor
COMPRESS_ENABLED = True
COMPRESS_URL = 'https://%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME
COMPRESS_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
COMPRESS_ROOT = '/static/'
COMPRESS_OUTPUT_DIR = 'static/CACHE'