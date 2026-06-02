# Ubuntu Network Configuration (Legacy interfaces file)

This method applies to older Ubuntu systems or those using the `ifupdown` networking stack.
For Ubuntu 18.04 and later, prefer [Netplan](./netplan.md).

## Table of Contents

- [Edit the Interfaces File](#edit-the-interfaces-file)
- [Configuration Example](#configuration-example)
- [Restart Networking](#restart-networking)

---

## Edit the Interfaces File

Open the network interfaces configuration file:

```bash
sudo nano /etc/network/interfaces
```

---

## Configuration Example

Add or edit the stanza for your network interface (replace `ens18` with your actual interface name):

```bash
auto ens18
iface ens18 inet static
  address 192.168.0.2
  netmask 255.255.255.0
  gateway 192.168.0.1
  dns-nameservers 89.207.128.252 89.207.130.252
```

To use DHCP instead of a static address:

```bash
auto ens18
iface ens18 inet dhcp
```

> Find your interface name with `ip link show` or `ip addr`.

---

## Restart Networking

Apply the new configuration by restarting the networking service:

```bash
sudo systemctl restart networking
```
