# Docker

## Table of Contents

- [Run a Container](#run-a-container)
- [Build an Image](#build-an-image)
- [Manage Containers](#manage-containers)
- [Docker Compose](#docker-compose)

---

## Run a Container

Run an interactive container with a volume mount (useful for Django project scaffolding):

```bash
sudo docker run -it --rm -v $(pwd):/code django bash
```

Inside the container:

```bash
cd /code
django-admin startproject <project_name>
exit
```

After scaffolding, edit the Django settings file:

```text
<project_name>/settings.py
```

- Under `INSTALLED_APPS`, add your app name.

Run the Django development server:

```bash
sudo docker run -t --rm \
  -p 0.0.0.0:5001:5000 \
  -v $(pwd):/code \
  -w /code/<project_name> \
  django \
  python manage.py runserver 0.0.0.0:5000
```

Run a container from an existing image by key (image ID or tag):

```bash
sudo docker run -it -p 0.0.0.0:5001:8000 <image_id_or_tag>
```

---

## Build an Image

Build a Docker image from the `Dockerfile` in the current directory:

```bash
sudo docker build .
```

List all locally available images:

```bash
sudo docker images
```

---

## Manage Containers

List running containers:

```bash
sudo docker ps
```

Stop a running container:

```bash
sudo docker stop <container_name>
```

Remove a stopped container:

```bash
sudo docker rm <container_name>
```

---

## Docker Compose

Start all services defined in `docker-compose.yml`:

```bash
sudo docker-compose up
```

Start in detached (background) mode:

```bash
sudo docker-compose up -d
```

Stop all running services:

```bash
sudo docker-compose down
```
