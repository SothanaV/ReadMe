# K3s: Move Data Directory to Another Location

This guide covers how to safely stop K3s, move its data directories to a new mount point, and create symlinks so K3s continues to work without reconfiguration.

Reference: [How to move K3s data to another location](https://mrkandreev.name/snippets/how_to_move_k3s_data_to_another_location/)

## Table of Contents

- [Stop K3s Services](#stop-k3s-services)
- [Move Data and Create Symlinks](#move-data-and-create-symlinks)
- [Start K3s Services](#start-k3s-services)

## Stop K3s Services

### Stop the server (master) node

```bash
systemctl status k3s
systemctl stop k3s
/usr/local/bin/k3s-killall.sh
```

### Stop agent (worker) nodes

```bash
systemctl status k3s-agent
systemctl stop k3s-agent
/usr/local/bin/k3s-killall.sh
```

## Move Data and Create Symlinks

Run this script on each node after stopping K3s. Adjust `/mnt/data_store` to match your target mount point.

```bash
#!/bin/bash
# Move K3s data directories to a new location and replace them with symlinks.
# Ref: https://mrkandreev.name/snippets/how_to_move_k3s_data_to_another_location/

mv /run/k3s/              /mnt/data_store/k3s/
mv /var/lib/kubelet/pods/ /mnt/data_store/k3s-pods/
mv /var/lib/rancher/      /mnt/data_store/k3s-rancher/

ln -s /mnt/data_store/k3s/         /run/k3s
ln -s /mnt/data_store/k3s-pods/    /var/lib/kubelet/pods
ln -s /mnt/data_store/k3s-rancher/ /var/lib/rancher
```

## Start K3s Services

### Start the server (master) node

```bash
systemctl start k3s
systemctl status k3s
```

### Start agent (worker) nodes

```bash
systemctl start k3s-agent
systemctl status k3s-agent
```
