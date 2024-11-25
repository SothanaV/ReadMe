# celery django
1. install celery
```bash
pip install celery[redis]
```

2. create `<PROJECT>/<PROJECT>/celery.py` alongside `settings.py`
```py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

3. add config in `settings.py`
```py
import os

...

CELERY_BROKER_URL = os.environ.get('REDIS_URI')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URI')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULE = {
    'check_health_every_10_minutes': {
        'task': 'app.tasks.check_use_survey',
        'schedule': int(os.environ.get('CELERY_SCHEDULE_TIME', 600)) # seconds
    },
}
```

4. create `<APP>/task.py`
```py
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
        'last_use': None
    })
```

5. add services in `docker-compose.yml`
```yml
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