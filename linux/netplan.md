# Network Configuration Using Netplan

Reference: <https://netplan.readthedocs.io/en/latest/netplan-yaml/>

## Table of Contents

- [Edit Configuration](#edit-configuration)
- [Configuration Example](#configuration-example)
- [Apply Configuration](#apply-configuration)

---

## Edit Configuration

Open the Netplan configuration file in a text editor:

```bash
sudo nano /etc/netplan/00-installer-config.yaml
```

> The filename may differ on your system. List available configs with `ls /etc/netplan/`.

---

## Configuration Example

The example below assigns static IP addresses to two network interfaces:

```yaml
network:
  version: 2
  ethernets:
    ens35:
      addresses:
        - 10.16.4.210/24
    ens36:
      addresses:
        - 10.16.5.210/24
```

### Example with gateway and DNS

```yaml
network:
  version: 2
  ethernets:
    ens33:
      addresses:
        - 192.168.1.100/24
      routes:
        - to: default
          via: 192.168.1.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
```

---

## Apply Configuration

After editing, apply the configuration:

```bash
sudo netplan apply
```

To test the configuration without permanently applying it (rolls back after 120 seconds if not confirmed):

```bash
sudo netplan try
```
