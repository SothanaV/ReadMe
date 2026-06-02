# Install Docker

## Table of Contents

- [Install](#install)
- [Post-Install Setup](#post-install-setup)
- [Verify Installation](#verify-installation)
- [Optional: ctop](#optional-ctop)

---

## Install

Add Docker's official GPG key and repository, then install the engine:

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install -y \
  docker-ce \
  docker-ce-cli \
  containerd.io \
  docker-buildx-plugin \
  docker-compose-plugin
```

---

## Post-Install Setup

Add your user to the `docker` group so you can run Docker without `sudo`:

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```

> You may need to log out and back in for group membership to take effect.

---

## Verify Installation

Check the Docker Compose plugin version:

```bash
docker compose version
```

Run the hello-world test image:

```bash
docker run hello-world
```

---

## Optional: ctop

`ctop` is a top-like interface for monitoring container metrics.

```bash
sudo wget https://github.com/bcicen/ctop/releases/download/v0.7.7/ctop-0.7.7-linux-amd64 \
  -O /usr/local/bin/ctop
sudo chmod +x /usr/local/bin/ctop
```

Run it with:

```bash
ctop
```
