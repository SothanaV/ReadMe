# Visualize Database Schema in Django

## Table of Contents

- [Install System Dependencies](#install-system-dependencies)
- [Install Python Packages](#install-python-packages)
- [Configure Django](#configure-django)
- [Generate Schema Diagrams](#generate-schema-diagrams)

---

## Install System Dependencies

### Ubuntu / Linux (native)

```bash
sudo apt install graphviz
```

### Dockerfile

```dockerfile
RUN apt-get install -y graphviz
```

---

## Install Python Packages

```bash
pip install django-extensions pydotplus
```

---

## Configure Django

Add `django_extensions` to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'django_extensions',
]
```

---

## Generate Schema Diagrams

Export the full schema (all apps):

```bash
python manage.py graph_models -a -g -o <image_file_name>.png
```

Export the schema for specific apps only:

```bash
python manage.py graph_models <app1> <app2> -o app1_app2.png
```
