# Setup NVIDIA Docker (Container Toolkit)

Enable GPU access inside Docker containers using the NVIDIA Container Toolkit.

## Table of Contents

- [Update the System](#update-the-system)
- [Install the NVIDIA Driver](#install-the-nvidia-driver)
- [Install Docker](#install-docker)
- [Install the NVIDIA Container Toolkit](#install-the-nvidia-container-toolkit)
- [Configure the Runtime](#configure-the-runtime)
- [Test GPU Access](#test-gpu-access)
- [Optional: Set cgroup Driver](#optional-set-cgroup-driver)

---

## Update the System

```bash
sudo apt update && sudo apt upgrade -y
```

---

## Install the NVIDIA Driver

Search for available driver versions:

```bash
apt search nvidia-driver
```

Install the appropriate version for your GPU:

```bash
sudo apt install -y nvidia-driver-<VERSION>
```

Verify the driver is loaded (a reboot may be required first):

```bash
nvidia-smi
```

---

## Install Docker

Follow the Docker installation guide: [docker-install.md](./docker-install.md)

---

## Install the NVIDIA Container Toolkit

Reference: [NVIDIA Container Toolkit install guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

### Add the NVIDIA repository

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
  | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
  | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
  | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

### Install the toolkit

```bash
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
```

---

## Configure the Runtime

Register the NVIDIA runtime with Docker and restart the daemon:

```bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

---

## Test GPU Access

Run a CUDA container to confirm the GPU is visible inside Docker:

```bash
sudo docker run --rm --gpus all \
  nvidia/cuda:12.6.3-base-ubuntu24.04 \
  nvidia-smi
```

---

## Optional: Set cgroup Driver

If your environment requires `cgroupfs` as the cgroup driver, add it to `/etc/docker/daemon.json`:

```json
{
  "runtimes": {
    "nvidia": {
      "args": [],
      "path": "nvidia-container-runtime"
    }
  },
  "exec-opts": ["native.cgroupdriver=cgroupfs"]
}
```

Restart Docker after editing:

```bash
sudo systemctl restart docker
```
