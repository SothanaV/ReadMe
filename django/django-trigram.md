# Django Trigram Search
### required
- postgresql
- django > 3

### step
- create model
```py
from django.db import models

class Key(models.Model):
    name = models.TextField()
```
- makemigrations
```sh
python manage.py makemigrations
```

- edit migration file eg `myApp/migrations/0001_initial.py`
```py
from django.contrib.postgres.operations import TrigramExtension, BtreeGinExtension

class Migration(migrations.Migration):

    ...

    operations = [
        ...
        TrigramExtension(), # add this
        ...
    ]

```
- migrate database
```sh
python manage.py migrate
```


# Usage
```py
from django.contrib.postgres.search import TrigramSimilarity

q = "test"
queryset = model.objects.annotate(
    similarity=TrigramSimilarity('name', q)
).filter(similarity__gt=0.3).order_by('-similarity')
print(queryset)
```

## Optimize
ref https://blacksheephacks.pl/optimizing-django-database-queries-part-2/

- create index `models.py`
```py
class Key(models.Model):
    name = models.TextField()

    class Meta:
        indexes = [
            GinIndex(
                fields=['name'],
                opclasses=['gin_trgm_ops'],
                name='name_trigram_idx'
            ),
        ]
```

- makemigrations
- edit migrations file
```py
from django.contrib.postgres.operations import  BtreeGinExtension
class Migration(migrations.Migration):

    ...

    operations = [
        ...
        BtreeGinExtension(), # add this
        ...
    ]
```