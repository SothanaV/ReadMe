# Celery with Django

## Table of Contents

- [Installation](#installation)
- [Celery Application](#celery-application)
- [Django Settings](#django-settings)
- [Task Definition](#task-definition)
- [Docker Compose Services](#docker-compose-services)

---

## Installation

```bash
pip install celery[redis]
```

---

## Celery Application

Create `<PROJECT>/<PROJECT>/celery.py` alongside `settings.py`:

```python
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

---

## Django Settings

Add the following configuration to `settings.py`:

```python
import os

# ...

CELERY_BROKER_URL = os.environ.get('REDIS_URI')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URI')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULE = {
    'check_health_every_10_minutes': {
        'task': 'app.tasks.check_use_survey',
        'schedule': int(os.environ.get('CELERY_SCHEDULE_TIME', 600)),  # seconds
    },
}
```

---

## Task Definition

Create `<APP>/tasks.py`:

```python
from celery import shared_task
from . import models

from datetime import timedelta
from django.utils.timezone import now


@shared_task
def check_use_survey():
    time = now() - timedelta(minutes=5)
    surveys = models.Survey.objects.filter(last_use__lte=time)
    surveys.update(**{
        'use_by': None,
        'last_use': None,
    })
```

---

## Docker Compose Services

Add the following services to `docker-compose.yml`:

```yaml
services:
  celery:
    container_name: ${PROJECT_NAME}-celery_worker
    build: ./backend
    command: celery -A backend worker --loglevel=info
    volumes:
      - ./backend:/backend
    env_file:
      - .env

  celery-beat:
    container_name: ${PROJECT_NAME}-celery_beat
    build: ./backend
    command: celery -A backend beat --loglevel=info
    volumes:
      - ./backend:/backend
    env_file:
      - .env
```
