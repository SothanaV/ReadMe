# Django Storage on Bucket
- install
```
pip install django-storages boto3
```

- edit in `settings.py`
```python
import os

INSTALLED_APPS = [
    ...
    'storages',
    ...
]

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_ENDPOINT_URL = os.environ.get('OSD_ENDPOINT')
AWS_ACCESS_KEY_ID = os.environ.get('OSD_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('OSD_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('OSD_BUCKET_NAME')
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
```

## if django version >= 4.2
- `DEFAULT_FILE_STORAGE` change to `STORAGES`
```python
STORAGES = {
    'default':{
        'BACKEND':'storages.backends.s3boto3.S3Boto3Storage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}
```
