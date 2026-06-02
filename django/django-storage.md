# Django Storage on Object Storage Bucket (S3-compatible)

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Django 4.2 and Later](#django-42-and-later)

---

## Installation

```bash
pip install django-storages boto3
```

---

## Configuration

Edit `settings.py`:

```python
import os

INSTALLED_APPS = [
    # ...
    'storages',
    # ...
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

---

## Django 4.2 and Later

The `DEFAULT_FILE_STORAGE` setting is deprecated in Django 4.2. Use the new `STORAGES` dict instead:

```python
STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}
```
