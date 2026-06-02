# ReadMe

Personal reference documentation for DevOps, infrastructure, and development workflows.

## Table of Contents

- [Linux](#linux)
- [Docker](#docker)
- [Kubernetes](#kubernetes)
- [Kedro + Airflow + K8s](#kedro--airflow--k8s)
- [Django](#django)
- [Python](#python)
- [Database](#database)
- [Network](#network)
- [Bucket / Storage](#bucket--storage)
- [Security](#security)
- [NVIDIA / GPU](#nvidia--gpu)
- [Proxmox](#proxmox)
- [Ansible](#ansible)
- [Git](#git)
- [Sothana Setup](#sothana-setup)
- [Utils](#utils)
- [Archive](#archive)

---

## Linux

| File | Description |
| ---- | ----------- |
| [command.md](linux/command.md) | Common Unix/Linux command reference |
| [setup_server.md](linux/setup_server.md) | Initial server setup (Docker, ctop) |
| [settingNetworkUbuntu.md](linux/settingNetworkUbuntu.md) | Static IP / network configuration on Ubuntu |
| [netplan.md](linux/netplan.md) | Netplan YAML network configuration |
| [ssh-key-gen.md](linux/ssh-key-gen.md) | Generate and deploy SSH keys |
| [ssh-tools.md](linux/ssh-tools.md) | SSH helper scripts and tools |
| [SambaServer.md](linux/SambaServer.md) | Set up a Samba file server |
| [mount-smb.md](linux/mount-smb.md) | Mount SMB/CIFS shares |
| [nfs.md](linux/nfs.md) | NFS server and client setup |
| [create-swap.md](linux/create-swap.md) | Create and enable a swap file |
| [expand-disk.md](linux/expand-disk.md) | Expand a disk partition and filesystem |
| [upgrade-ubuntu.md](linux/upgrade-ubuntu.md) | Upgrade Ubuntu to a new release |
| [CreateSuperuserUbuntu.md](linux/CreateSuperuserUbuntu.md) | Create a sudo user on Ubuntu |
| [log-check.md](linux/log-check.md) | Check logs with journalctl, systemctl, supervisorctl |
| [io-test.md](linux/io-test.md) | Disk I/O benchmarking with fio |
| [cuda-benchmark.md](linux/cuda-benchmark.md) | CUDA GPU benchmark |
| [Unrar.md](linux/Unrar.md) | Extract RAR archives |
| [vm_proxy_setup.md](linux/vm_proxy_setup.md) | VM proxy setup (Tinyproxy / SOCKS5) |
| [proxmox-cloudinit-vm.md](linux/proxmox-cloudinit-vm.md) | Create cloud-init VMs on Proxmox |
| [report-server-linux.md](linux/report-server-linux.md) | Server resource reporting script |

---

## Docker

| File | Description |
| ---- | ----------- |
| [docker-install.md](docker/docker-install.md) | Install Docker Engine on Ubuntu |
| [docker.md](docker/docker.md) | Docker command reference |
| [docker-compose.md](docker/docker.md) | Docker Compose usage (see docker.md) |
| [move-docker.md](docker/move-docker.md) | Move Docker data directory |
| [change-docker-network.md](docker/change-docker-network.md) | Change Docker default bridge network subnet |
| [setup_nvidia-docker.md](docker/setup_nvidia-docker.md) | Set up NVIDIA Container Toolkit |

---

## Kubernetes

| File | Description |
| ---- | ----------- |
| [k3s.md](kubernetes/k3s.md) | K3s tips: etcd restore, resource limits |
| [k3s-install-ansible.md](kubernetes/k3s-install-ansible.md) | Install K3s via Ansible |
| [k3s-backup-etcd.md](kubernetes/k3s-backup-etcd.md) | Back up and restore K3s etcd |
| [k3s-move-data.md](kubernetes/k3s-move-data.md) | Move K3s data directory |
| [helm-install.md](kubernetes/helm-install.md) | Install Helm |
| [ingress-cross-namespace.md](kubernetes/ingress-cross-namespace.md) | Cross-namespace ingress routing |
| [kube-cheatcheet.md](kubernetes/kube-cheatcheet.md) | kubectl cheat sheet |
| [kube-tips.md](kubernetes/kube-tips.md) | Kubernetes tips and tricks |

---

## Kedro + Airflow + K8s

| File | Description |
| ---- | ----------- |
| [kedro-airflow2_4_1-k8s.md](kedro-airflow-k8s/kedro-airflow2_4_1-k8s.md) | Kedro + Airflow 2.4.1 on K8s |
| [kedro-airflow2_10_3-k8s.md](kedro-airflow-k8s/kedro-airflow2_10_3-k8s.md) | Kedro + Airflow 2.10.3 on K8s |
| [kedro-airflow3_0_2-k8s.md](kedro-airflow-k8s/kedro-airflow3_0_2-k8s.md) | Kedro + Airflow 3.0.2 on K8s |

---

## Django

| File | Description |
| ---- | ----------- |
| [ReadMe_Django.md](django/ReadMe_Django.md) | Django quick-start reference |
| [django-setup.md](django/django-setup.md) | Django project setup |
| [django-celery.md](django/django-celery.md) | Celery integration with Django |
| [django-storage.md](django/django-storage.md) | File storage backends (S3, GCS) |
| [django-trigram.md](django/django-trigram.md) | Trigram similarity search |
| [django-jupyter.md](django/django-jupyter.md) | Use Jupyter with Django shell |
| [django-old-problem.md](django/django-old-problem.md) | Known issues and fixes |
| [visualize_db_django.md](django/visualize_db_django.md) | Visualize Django database schema |

---

## Python

| File | Description |
| ---- | ----------- |
| [conda-env.md](python/conda-env.md) | Conda environment management |
| [jupyter_set_passwd.md](python/jupyter_set_passwd.md) | Set Jupyter Notebook password |
| [airflow-command.md](python/airflow-command.md) | Airflow CLI command reference |
| [airflow-v2-oauth.md](python/airflow-v2-oauth.md) | Airflow v2 OAuth2 setup |
| [airflow-v3-oauth.md](python/airflow-v3-oauth.md) | Airflow v3 OAuth2 setup |
| [superset.md](python/superset.md) | Apache Superset setup |
| [sphinx.md](python/sphinx.md) | Sphinx documentation setup |
| [async2sync.md](python/async2sync.md) | Run async code from sync context |
| [check-gpu.md](python/check-gpu.md) | Check GPU availability in Python |
| [test-ollama.md](python/test-ollama.md) | Test Ollama inference locally |
| [oracle.md](python/oracle.md) | Oracle DB connection setup |
| [python-smb-fs.md](python/python-smb-fs.md) | Access SMB shares from Python |
| [upload-to-pip.md](python/upload-to-pip.md) | Publish a package to PyPI |

---

## Database

| File | Description |
| ---- | ----------- |
| [postgresql-vector.md](database/postgresql-vector.md) | pgvector extension setup |
| [clickhouse.md](database/clickhouse.md) | ClickHouse installation and usage |

---

## Network

| File | Description |
| ---- | ----------- |
| [nginx-proxy.md](network/nginx-proxy.md) | Nginx reverse proxy configuration |
| [mikrotik-ppoe.md](network/mikrotik-ppoe.md) | MikroTik PPPoE setup |
| [redirect/README.md](network/redirect/README.md) | Nginx HTTP redirect setup |

---

## Bucket / Storage

| File | Description |
| ---- | ----------- |
| [gcsfuse.md](bucket/gcsfuse.md) | Mount GCS bucket with gcsfuse |
| [gcp-bucket-CORS.md](bucket/gcp-bucket-CORS.md) | Configure CORS on a GCS bucket |
| [gcp_ssh.md](bucket/gcp_ssh.md) | GCP SSH key setup |
| [s3fs.md](bucket/s3fs.md) | Mount S3 bucket with s3fs |

---

## Security

| File | Description |
| ---- | ----------- |
| [sonarqube-plugin.md](sec/sonarqube-plugin.md) | Install SonarQube plugins |
| [sonarqube-ldap.md](sec/sonarqube-ldap.md) | SonarQube LDAP authentication |

---

## NVIDIA / GPU

| File | Description |
| ---- | ----------- |
| [gpu-grafana-dashboard.md](nvidia/gpu-grafana-dashboard.md) | NVIDIA GPU Grafana dashboard setup |
| [dcgmi.md](nvidia/dcgmi.md) | DCGM and dcgmi GPU monitoring |

---

## Proxmox

| File | Description |
| ---- | ----------- |
| [proxmox-backup-server.md](proxmox/proxmox-backup-server.md) | Proxmox Backup Server setup |

---

## Ansible

| File | Description |
| ---- | ----------- |
| [README.md](ansible/README.md) | Ansible installation and usage guide |

---

## Git

| File | Description |
| ---- | ----------- |
| [git.md](git.md) | Git command reference and workflow guide |

---

## Sothana Setup

| File | Description |
| ---- | ----------- |
| [package-ubuntu-forwork.md](sothana/package-ubuntu-forwork.md) | Ubuntu packages for work environment |

---

## Utils

| File | Description |
| ---- | ----------- |
| [network-explor/README.md](utils/network-explor/README.md) | Network exploration tool setup |

---

## Archive

Older documentation kept for reference.

| File | Description |
| ---- | ----------- |
| [arduino_lib.md](_archive/arduino_lib.md) | Arduino library references |
| [build_yolo_v4.md](_archive/build_yolo_v4.md) | Build YOLOv4 from source |
| [install_opencv_4.3.0.md](_archive/install_opencv_4.3.0.md) | Install OpenCV 4.3.0 |
| [ipcam.md](_archive/ipcam.md) | IP camera streaming with ffmpeg |
| [Ocr_tesseract.md](_archive/Ocr_tesseract.md) | Tesseract OCR setup |
| [openstack.md](_archive/openstack.md) | OpenStack setup notes |
