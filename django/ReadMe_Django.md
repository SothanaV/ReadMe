# Django Quick Start

## Table of Contents

- [Install Python](#install-python)
- [Install Django](#install-django)
- [Start a Project](#start-a-project)
- [Create an App](#create-an-app)
- [Database](#database)
- [Run the Development Server](#run-the-development-server)
- [Create a Superuser](#create-a-superuser)

---

## Install Python

Install Anaconda or a standalone Python distribution from <https://www.python.org/downloads/>.

---

## Install Django

```bash
# Using conda
conda install django

# Or using pip
pip install django
```

---

## Start a Project

สร้างโปรเจค (Create a project):

```bash
django-admin startproject <project_name>
```

---

## Create an App

สร้างแอพ (Create an app):

```bash
python manage.py startapp <app_name>
```

Register the app in `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    '<app_name>',
]
```

---

## Database

เตรียมสร้างฐานข้อมูล (Prepare migrations):

```bash
python manage.py makemigrations
```

สร้างฐานข้อมูล (Apply migrations):

```bash
python manage.py migrate
```

---

## Run the Development Server

```bash
python manage.py runserver
```

---

## Create a Superuser

```bash
python manage.py createsuperuser
```
