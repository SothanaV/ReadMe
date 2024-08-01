# Postgresql vector

- start postgresql vector using docker `docker-compose.yml`
```yml
volumes:
    db: {}

services: 
    db:
        container_name: db
        image: pgvector/pgvector:pg16
        volumes:
            - db:/var/lib/postgresql/data
        environments:
            - POSTGRES_DB: 'vector'
            - POSTGRES_USER: 'vector'
            - POSTGRES_PASSWORD: 'vector_pass'
```

# Django
- start django project and create app
- create models in ```app/models.py```
```python
from django.db import models
from pgvector.django import VectorField
...

class Embedding(models.Model):
    ...
    name = models.TextField()
    vector = VectorField()
```
- makemigrations
```sh
python manage.py makemigrations
```
- edit migrations ```app/migrations/0001_initial.py```
```python
...
from pgvector.django import VectorExtension
class Migration(migrations.Migration):
    ...
    operations = [
        VectorExtension(), # add this for vector extension
        ...
    ]
```
- migrate
```sh
python manage.py migrate
```

## django use vector
- create
```py
from vector.models import Embedding
Embedding.objects.create(**{
    'name': "text",
    'data': [1,2,3,4] # list or np array
})
```

- query
```py
from pgvector.django import CosineDistance

test_vec = [1,2,2,5]
queryset = Embedding.objects.order_by(CosineDistance('vector', test_vec))[:5]
print(queryset)
```

# Sqlalchemy
```py
# import lib
import sqlalchemy
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import Column, Text, Integer
from pgvector.sqlalchemy import Vector
import pandas as pd

# define connection and test connection
con_str = f'postgresql://user:password@host:port/db'
engine = sqlalchemy.create_engine(con_str, echo=False)
engine.connect()

# create vector extension
session = Session(engine)
session.execute(sqlalchemy.text('CREATE EXTENSION IF NOT EXISTS vector'))

# check extension
```
|    |     oid | extname   |   extowner |   extnamespace | extrelocatable   | extversion   | extconfig   | extcondition   |
|---:|--------:|:----------|-----------:|---------------:|:-----------------|:-------------|:------------|:---------------|
|  0 |   13561 | plpgsql   |         10 |             11 | False            | 1.0          |             |                |
|  1 |  733197 | vector    |         10 |           2200 | True             | 0.5.1        |             |                |
```py
# define Table
Base = declarative_base()
class Embedding(Base):
    __tablename__ = 'embedding'
    idx = Column(Integer, primary_key=True)
    vector = Column(Vector()) 

# create table
Base.metadata.create_all(engine)

# check schema
pd.read_sql_query("""
select column_name, data_type, character_maximum_length, column_default, is_nullable
from INFORMATION_SCHEMA.COLUMNS where table_name = 'master';
""", con_str)
```
|    | column_name   | data_type    | character_maximum_length   | column_default                    | is_nullable   |
|---:|:--------------|:-------------|:---------------------------|:----------------------------------|:--------------|
|  0 | idx           | integer      |                            | nextval('data_idx_seq'::regclass) | NO            |
|  1 | vector        | USER-DEFINED |                            |                                   | YES           |

```py
# import data
item = Embedding(**{
    'idx': 1,
    'vector': [1,2,3,4]
})
session.add(item)
session.commit() 

# query
test_vec = [1,2,3,3]
data = session.query(Embedding).order_by(Embedding.data.l2_distance(test_vec)).all()
print(data) 
```