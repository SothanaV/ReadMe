# Change the Default Docker Network

When Docker's default bridge IP ranges conflict with existing network services, you can override the default address pools to use a custom subnet.

## Table of Contents

- [Configure the Default Address Pool](#configure-the-default-address-pool)
- [Restart Docker](#restart-docker)
- [Verify the New Subnet](#verify-the-new-subnet)

---

## Configure the Default Address Pool

Edit the Docker daemon configuration file:

```bash
sudo nano /etc/docker/daemon.json
```

Add or merge the following configuration (adjust the `base` and `size` values to suit your network):

```json
{
  "default-address-pools": [
    { "base": "10.10.0.0/16", "size": 24 }
  ]
}
```

- `base`: The parent CIDR block from which subnets are allocated.
- `size`: The prefix length of each individual network subnet (e.g., `24` produces `/24` subnets).

---

## Restart Docker

```bash
sudo service docker restart
```

---

## Verify the New Subnet

Create a test network and inspect its subnet to confirm the new pool is in effect:

```bash
docker network create foo
docker network inspect foo | grep Subnet
```

Expected output:

```text
"Subnet": "10.10.1.0/24"
```

Remove the test network when done:

```bash
docker network rm foo
```
