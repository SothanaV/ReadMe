# PostgreSQL with pgvector

[pgvector](https://github.com/pgvector/pgvector) is a PostgreSQL extension for storing and querying vector embeddings. It supports exact and approximate nearest-neighbor search using L2 distance, cosine distance, and inner product.

## Start PostgreSQL with pgvector Using Docker Compose

Create a `docker-compose.yml` file:

```yaml
volumes:
  db: {}

services:
  db:
    container_name: db
    image: pgvector/pgvector:pg16
    volumes:
      - db:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: vector
      POSTGRES_USER: vector
      POSTGRES_PASSWORD: vector_pass
```

```bash
docker compose up -d
```

## Django Integration

### 1. Start a Django Project and Create an App

```bash
django-admin startproject myproject
cd myproject
python manage.py startapp myapp
```

### 2. Define a Model with a Vector Field

Edit `myapp/models.py`:

```python
from django.db import models
from pgvector.django import VectorField

class Embedding(models.Model):
    name = models.TextField()
    vector = VectorField(dimensions=4)
```

### 3. Generate Migrations

```bash
python manage.py makemigrations
```

### 4. Enable the Vector Extension in the Migration

Edit the generated migration file `myapp/migrations/0001_initial.py` to install the `vector` extension before creating the table:

```python
from pgvector.django import VectorExtension
from django.db import migrations

class Migration(migrations.Migration):

    operations = [
        VectorExtension(),  # enables the pgvector extension
        # ... auto-generated operations below ...
    ]
```

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Insert and Query Vectors

**Insert a record:**

```python
from myapp.models import Embedding

Embedding.objects.create(name="example", vector=[1, 2, 3, 4])
```

**Query by cosine distance (nearest neighbors):**

```python
from pgvector.django import CosineDistance

query_vector = [1, 2, 2, 5]
results = Embedding.objects.order_by(CosineDistance('vector', query_vector))[:5]
print(results)
```

## SQLAlchemy Integration

### Setup and Connection

```python
import sqlalchemy
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import Column, Text, Integer
from pgvector.sqlalchemy import Vector
import pandas as pd

# Define connection string
connection_string = 'postgresql://user:password@host:port/db'
engine = sqlalchemy.create_engine(connection_string, echo=False)

# Test the connection
with engine.connect() as conn:
    print("Connection successful")
```

### Enable the pgvector Extension

```python
session = Session(engine)
session.execute(sqlalchemy.text('CREATE EXTENSION IF NOT EXISTS vector'))
session.commit()
```

Verify the extension is installed:

```python
pd.read_sql_query("SELECT * FROM pg_extension;", connection_string)
```

Expected output (abridged):

| oid    | extname | extversion |
|--------|---------|------------|
| 13561  | plpgsql | 1.0        |
| 733197 | vector  | 0.5.1      |

### Define a Table Model

```python
Base = declarative_base()

class Embedding(Base):
    __tablename__ = 'embedding'
    idx = Column(Integer, primary_key=True, autoincrement=True)
    vector = Column(Vector(4))

# Create the table
Base.metadata.create_all(engine)
```

Verify the schema:

```python
pd.read_sql_query("""
    SELECT column_name, data_type, column_default, is_nullable
    FROM information_schema.columns
    WHERE table_name = 'embedding';
""", connection_string)
```

Expected output:

| column_name | data_type    | column_default                            | is_nullable |
|-------------|--------------|-------------------------------------------|-------------|
| idx         | integer      | nextval('embedding_idx_seq'::regclass)    | NO          |
| vector      | USER-DEFINED |                                           | YES         |

### Insert and Query Vectors

**Insert a record:**

```python
item = Embedding(idx=1, vector=[1, 2, 3, 4])
session.add(item)
session.commit()
```

**Query by L2 distance (nearest neighbors):**

```python
query_vector = [1, 2, 3, 3]
results = session.query(Embedding).order_by(Embedding.vector.l2_distance(query_vector)).all()
print(results)
```

## Performance Optimization

For large datasets, create an approximate nearest-neighbor index to speed up queries:

```sql
-- IVFFlat index for L2 distance
CREATE INDEX ON embedding USING ivfflat (vector vector_l2_ops) WITH (lists = 100);

-- IVFFlat index for cosine distance
CREATE INDEX ON embedding USING ivfflat (vector vector_cosine_ops) WITH (lists = 100);
```

Set the number of probes at query time to balance speed and recall:

```sql
SET ivfflat.probes = 10;
```
