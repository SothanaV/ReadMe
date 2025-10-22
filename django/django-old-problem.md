# Login Oauth varchar too long(30)
```sh
Internal Server Error: /oauth/complete/dsmauth/
Traceback (most recent call last):
  File "/usr/local/lib/python3.7/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
psycopg2.errors.StringDataRightTruncation: value too long for type character varying(30)


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/local/lib/python3.7/site-packages/django/core/handlers/exception.py", line 34, in inner
    response = get_response(request)
  File "/usr/local/lib/python3.7/site-packages/django/core/handlers/base.py", line 115, in _get_response
    response = self.process_exception_by_middleware(e, request)
  File "/usr/local/lib/python3.7/site-packages/django/core/handlers/base.py", line 113, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "/usr/local/lib/python3.7/site-packages/django/views/decorators/cache.py", line 44, in _wrapped_view_func
    response = view_func(request, *args, **kwargs)
  File "/usr/local/lib/python3.7/site-packages/django/views/decorators/csrf.py", line 54, in wrapped_view
    return view_func(*args, **kwargs)
  File "/usr/local/lib/python3.7/site-packages/social_django/utils.py", line 46, in wrapper
    return func(request, backend, *args, **kwargs)
  File "/usr/local/lib/python3.7/site-packages/dsmauth/complete.py", line 31, in complete
    *args, **kwargs)
  File "/usr/local/lib/python3.7/site-packages/social_core/actions.py", line 45, in do_complete
    user = backend.complete(user=user, *args, **kwargs)
  File "/usr/local/lib/python3.7/site-packages/social_core/backends/base.py", line 40, in complete
    return self.auth_complete(*args, **kwargs)
  File "/usr/local/lib/python3.7/site-packages/social_core/utils.py", line 247, in wrapper
    return func(*args, **kwargs)
  File "/usr/local/lib/python3.7/site-packages/social_core/backends/oauth.py", line 402, in auth_complete
    *args, **kwargs)
  File "/usr/local/lib/python3.7/site-packages/social_core/utils.py", line 247, in wrapper
    return func(*args, **kwargs)
  File "/usr/local/lib/python3.7/site-packages/social_core/backends/oauth.py", line 413, in do_auth
    return self.strategy.authenticate(*args, **kwargs)
  File "/usr/local/lib/python3.7/site-packages/social_django/strategy.py", line 105, in authenticate
    return authenticate(*args, **kwargs)
  File "/usr/local/lib/python3.7/site-packages/django/contrib/auth/__init__.py", line 73, in authenticate
    user = backend.authenticate(request, **credentials)
  File "/usr/local/lib/python3.7/site-packages/social_core/backends/base.py", line 80, in authenticate
    return self.pipeline(pipeline, *args, **kwargs)
  File "/usr/local/lib/python3.7/site-packages/social_core/backends/base.py", line 83, in pipeline
    out = self.run_pipeline(pipeline, pipeline_index, *args, **kwargs)
  File "/usr/local/lib/python3.7/site-packages/social_core/backends/base.py", line 113, in run_pipeline
    result = func(*args, **out) or {}
  File "/usr/local/lib/python3.7/site-packages/social_core/pipeline/user.py", line 122, in user_details
    strategy.storage.user.changed(user)
  File "/usr/local/lib/python3.7/site-packages/social_django/storage.py", line 16, in changed
    user.save()
  File "/usr/local/lib/python3.7/site-packages/django/contrib/auth/base_user.py", line 66, in save
    super().save(*args, **kwargs)
  File "/usr/local/lib/python3.7/site-packages/django/db/models/base.py", line 741, in save
    force_update=force_update, update_fields=update_fields)
  File "/usr/local/lib/python3.7/site-packages/django/db/models/base.py", line 779, in save_base
    force_update, using, update_fields,
  File "/usr/local/lib/python3.7/site-packages/django/db/models/base.py", line 851, in _save_table
    forced_update)
  File "/usr/local/lib/python3.7/site-packages/django/db/models/base.py", line 900, in _do_update
    return filtered._update(values) > 0
  File "/usr/local/lib/python3.7/site-packages/django/db/models/query.py", line 760, in _update
    return query.get_compiler(self.db).execute_sql(CURSOR)
  File "/usr/local/lib/python3.7/site-packages/django/db/models/sql/compiler.py", line 1429, in execute_sql
    cursor = super().execute_sql(result_type)
  File "/usr/local/lib/python3.7/site-packages/django/db/models/sql/compiler.py", line 1100, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.7/site-packages/django/db/backends/utils.py", line 99, in execute
    return super().execute(sql, params)
  File "/usr/local/lib/python3.7/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(sql, params, many=False, executor=self._execute)
  File "/usr/local/lib/python3.7/site-packages/django/db/backends/utils.py", line 76, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/usr/local/lib/python3.7/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
  File "/usr/local/lib/python3.7/site-packages/django/db/utils.py", line 89, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.7/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
django.db.utils.DataError: value too long for type character varying(30)

[20/Oct/2025 15:58:58] "GET /oauth/complete/dsmauth/?redirect_state=2N3nLKY6OFSaHKr7eMMcbbmXBvX5AwA3&code=A476ChNGgggc1Wt26ic6DW8XHydDW8&state=2N3nLKY6OFSaHKr7eMMcbbmXBvX5AwA3 HTTP/1.1" 500 256635
```
- edit `/usr/local/lib/python3.7/site-packages/django/contrib/auth/models.py`

```
Class AbstractUser:
    ...
    first_name = model.CharField(max_lenth=60 ) # current = 30
```

- migrate database
```
python manage.py makemigrations
python manage.py migrate
```