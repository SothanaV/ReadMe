# Django Known Issues and Fixes

## Table of Contents

- [OAuth Login: varchar Too Long (30)](#oauth-login-varchar-too-long-30)

---

## OAuth Login: varchar Too Long (30)

### Problem

When completing an OAuth login flow, a `DataError` is raised because the `first_name` field on Django's `AbstractUser` model is defined as `VARCHAR(30)`, which is too short for some OAuth provider values.

```text
Internal Server Error: /oauth/complete/dsmauth/
...
psycopg2.errors.StringDataRightTruncation: value too long for type character varying(30)
...
django.db.utils.DataError: value too long for type character varying(30)
```

**Full traceback:**

```text
Traceback (most recent call last):
  File "/usr/local/lib/python3.7/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
psycopg2.errors.StringDataRightTruncation: value too long for type character varying(30)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/local/lib/python3.7/site-packages/social_core/pipeline/user.py", line 122, in user_details
    strategy.storage.user.changed(user)
  File "/usr/local/lib/python3.7/site-packages/social_django/storage.py", line 16, in changed
    user.save()
  ...
django.db.utils.DataError: value too long for type character varying(30)
```

### Fix

Edit `/usr/local/lib/python3.7/site-packages/django/contrib/auth/models.py` and increase the `max_length` on the `first_name` field in `AbstractUser`:

```python
class AbstractUser:
    # ...
    first_name = models.CharField(max_length=60)  # was 30
```

Then apply the database migration:

```bash
python manage.py makemigrations
python manage.py migrate
```

> **Note:** Editing library source files directly is not recommended for production. A better approach is to create a custom user model that extends `AbstractUser` and overrides the `first_name` field with the desired `max_length`.
