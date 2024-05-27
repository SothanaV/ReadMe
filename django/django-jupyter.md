# Django with jupyter shell plus
- create jupyter notebook password <a href="jupyter_set_passwd.md"> Here </a>

- install django extension
```
    pip install django-extensions
```
- add config in ```settings.py```
```python
INSTALLED_APPS = [
    ...
    'django_extensions',
   ...
]

NOTEBOOK_ARGUMENTS = [
    "--ip",
    "0.0.0.0",
    "--allow-root",
    "--no-browser",
    "--notebook-dir=/backend",
    "--config=/config/jupyter_notebook_config.json",
]
```

- run jupyter django shellplus with command
```
    python manage.py shell_plus --notebook
```

```optional if use docker```

```docker
    notebook:
        build: ./backend
        command: sh runjupyter.sh
        volumes: 
            - ./backend:/backend
            - ./jupyter_notebook_config.json:/config/jupyter_notebook_config.json
        ports: 
            - 8888:8888
        env_file: 
            - .env
```