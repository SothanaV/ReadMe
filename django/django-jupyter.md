# Django with Jupyter Shell Plus

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Shell](#running-the-shell)
- [Docker Setup (Optional)](#docker-setup-optional)

---

## Prerequisites

Create a Jupyter Notebook password before proceeding. See [jupyter_set_passwd.md](../python/jupyter_set_passwd.md) for instructions.

---

## Installation

Install the `django-extensions` package:

```bash
pip install django-extensions
```

---

## Configuration

Add the following to `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'django_extensions',
    # ...
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

---

## Running the Shell

Launch Jupyter with the Django shell_plus kernel:

```bash
python manage.py shell_plus --notebook
```

---

## Docker Setup (Optional)

Add a notebook service to `docker-compose.yml`:

```yaml
services:
  notebook:
    build: ./backend
    command: sh runjupyter.sh
    volumes:
      - ./backend:/backend
      - ./jupyter_notebook_config.json:/config/jupyter_notebook_config.json
    ports:
      - "8888:8888"
    env_file:
      - .env
```
