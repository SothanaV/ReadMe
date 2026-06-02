# Django Trigram Search

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Performance Optimization](#performance-optimization)

---

## Requirements

- PostgreSQL
- Django 3 or later

---

## Setup

### 1. Create the Model

```python
from django.db import models


class Key(models.Model):
    name = models.TextField()
```

### 2. Generate Migrations

```bash
python manage.py makemigrations
```

### 3. Edit the Migration File

Open the generated migration file (e.g., `myApp/migrations/0001_initial.py`) and add the `TrigramExtension`:

```python
from django.contrib.postgres.operations import TrigramExtension, BtreeGinExtension


class Migration(migrations.Migration):

    # ...

    operations = [
        # ...
        TrigramExtension(),  # add this
        # ...
    ]
```

### 4. Apply the Migration

```bash
python manage.py migrate
```

---

## Usage

```python
from django.contrib.postgres.search import TrigramSimilarity

q = "test"
queryset = Key.objects.annotate(
    similarity=TrigramSimilarity('name', q)
).filter(similarity__gt=0.3).order_by('-similarity')

print(queryset)
```

---

## Performance Optimization

Reference: <https://blacksheephacks.pl/optimizing-django-database-queries-part-2/>

### 1. Add a GIN Index to the Model

```python
from django.contrib.postgres.indexes import GinIndex
from django.db import models


class Key(models.Model):
    name = models.TextField()

    class Meta:
        indexes = [
            GinIndex(
                fields=['name'],
                opclasses=['gin_trgm_ops'],
                name='name_trigram_idx',
            ),
        ]
```

### 2. Generate and Edit the Migration

Run makemigrations, then open the generated migration file and add `BtreeGinExtension`:

```python
from django.contrib.postgres.operations import BtreeGinExtension


class Migration(migrations.Migration):

    # ...

    operations = [
        # ...
        BtreeGinExtension(),  # add this
        # ...
    ]
```

### 3. Apply the Migration

```bash
python manage.py migrate
```
