# OpenStack (DevStack)

> **Archived** — Instructions for deploying a single-node OpenStack environment using DevStack.

## Prerequisites

Update and upgrade the system, then create a dedicated `stack` user:

```bash
sudo apt update -y && sudo apt upgrade -y
sudo adduser stack --disabled-password
echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
su - stack
```

## Install DevStack

```bash
sudo apt install git -y
git clone https://git.openstack.org/openstack-dev/devstack
cd devstack
```

## Configure `local.conf`

Create a `local.conf` file in the `devstack` directory with the following content. Replace `<server-ip-address>` with the actual IP address of your server or VM (obtained via `ip addr`):

```ini
[[local|localrc]]

# Passwords for Keystone, Database, RabbitMQ, and Services
ADMIN_PASSWORD=StrongAdminSecret
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD

# Host IP — get your server/VM IP address from: ip addr
HOST_IP=<server-ip-address>
```

## Deploy

```bash
./stack.sh
```

The deployment process takes 15–30 minutes depending on network speed and hardware.

## Default Credentials

| Field    | Value               |
| -------- | ------------------- |
| Users    | `admin`, `demo`     |
| Password | `StrongAdminSecret` |

## Access the Dashboard

Once deployment is complete, open a browser and navigate to:

```text
http://<server-ip-address>/dashboard
```

## References

- [DevStack Documentation](https://docs.openstack.org/devstack/latest/)
- [OpenStack Official Site](https://www.openstack.org/)
