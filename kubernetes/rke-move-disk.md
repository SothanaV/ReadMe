# RKE2: Move containerd Data to Another Disk

This guide covers how to safely stop RKE2, copy the containerd data directory to a new disk, and bind-mount the new location back to the original path so RKE2 keeps working without reconfiguration.

## Table of Contents

- [Stop RKE2](#stop-rke2)
- [Copy containerd Data](#copy-containerd-data)
- [Clear the Original Data](#clear-the-original-data)
- [Persist the Bind Mount](#persist-the-bind-mount)
- [Mount and Restart](#mount-and-restart)
- [Verify](#verify)

## Stop RKE2

Stop the service on the node before touching any data.

### Agent (worker) node

```bash
systemctl status rke2-agent
systemctl stop rke2-agent
```

### Server (master) node

```bash
systemctl status rke2-server
systemctl stop rke2-server
```

## Copy containerd Data

Create the target directory on the new disk and copy the existing containerd data with `rsync`, preserving permissions, ownership, hard links, ACLs, and extended attributes.

```bash
sudo mkdir -p /mnt/new-disk/containerd

sudo rsync -aHAX --info=progress2 \
  /var/lib/rancher/rke2/agent/containerd/ \
  /mnt/new-disk/containerd/
```

> The trailing slashes matter: they copy the *contents* of the source directory into the destination.

## Clear the Original Data

Once the copy is verified, free up space on the original disk so the bind mount has an empty mount point.

```bash
sudo rm -rf /var/lib/rancher/rke2/agent/containerd/*
```

## Persist the Bind Mount

Add a bind-mount entry to `/etc/fstab` so the new disk is remounted at the original path on every boot.

```bash
sudo nano /etc/fstab
```

Append the following line:

```fstab
/mnt/new-disk/containerd /var/lib/rancher/rke2/agent/containerd none bind 0 0
```

> Make sure the new disk itself is mounted (via its own `fstab` entry) **before** this bind entry, otherwise `mount -a` at boot may fail to resolve the source.

## Mount and Restart

```bash
sudo mount -a
sudo systemctl start rke2-agent
```

Use `rke2-server` instead of `rke2-agent` on server nodes.

## Verify

Confirm the bind mount is active and RKE2 came back up cleanly:

```bash
findmnt /var/lib/rancher/rke2/agent/containerd
systemctl status rke2-agent
journalctl -u rke2-agent -f
```
