# Server Setup Guide

Initial setup for a Linux server: Docker, Docker Compose, and ctop.

## Table of Contents

- [Install Docker](#install-docker)
- [Install Docker Compose](#install-docker-compose)
- [Install ctop](#install-ctop)

---

## Install Docker

```bash
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add the Docker repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

sudo apt update
sudo apt install docker-ce

# Verify Docker is running
sudo systemctl status docker

# Allow your user to run Docker without sudo
sudo groupadd docker
sudo usermod -aG docker ${USER}
newgrp docker

# Verify
id -nG
docker --version
docker run hello-world
```

> **Note:** The official recommended install method is the convenience script from <https://get.docker.com> or the Docker APT repository. The steps above use the legacy `apt-key` approach which is deprecated in newer Ubuntu versions. See [Docker docs](https://docs.docker.com/engine/install/ubuntu/) for the current method.

---

## Install Docker Compose

The command below installs Docker Compose v2 (standalone binary). Replace the version number as needed.

```bash
# Check the latest version at https://github.com/docker/compose/releases
sudo curl -L \
  "https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

docker-compose --version
```

> Alternatively, Docker Compose v2 is available as a Docker plugin via `sudo apt install docker-compose-plugin`, usable as `docker compose` (without the hyphen).

---

## Install ctop

`ctop` is a top-like interface for Docker container metrics.

```bash
echo "deb http://packages.azlux.fr/debian/ buster main" | sudo tee /etc/apt/sources.list.d/azlux.list
wget -qO - https://azlux.fr/repo.gpg.key | sudo apt-key add -
sudo apt update
sudo apt install docker-ctop
```

Run it:

```bash
ctop
```
