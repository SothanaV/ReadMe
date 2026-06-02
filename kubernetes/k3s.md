# K3s Operations

## Table of Contents

- [Restore etcd from a Local Snapshot](#restore-etcd-from-a-local-snapshot)
- [Adjust Kubelet Resource Limits](#adjust-kubelet-resource-limits)

## Restore etcd from a Local Snapshot

> **Warning:** This resets the cluster to the state captured in the snapshot. Ensure all agents are stopped and that you are running this on the primary server node.

### Step 1: Stop the K3s service

```bash
systemctl stop k3s
```

### Step 2: Locate the desired snapshot

Snapshots are stored at:

```text
/var/lib/rancher/k3s/server/db/snapshots/
```

### Step 3: Restore etcd from the snapshot

Replace `<SNAPSHOT_FILENAME>` with the actual snapshot file name found in step 2.

```bash
k3s server \
  --cluster-reset \
  --cluster-reset-restore-path=/var/lib/rancher/k3s/server/db/snapshots/<SNAPSHOT_FILENAME> \
  --etcd-arg=quota-backend-bytes=$((8*1024*1024*1024))
```

### Step 4: Verify the server starts correctly

Check what arguments K3s is normally started with:

```bash
cat /etc/systemd/system/k3s.service
```

Start K3s manually to monitor the logs and confirm startup:

```bash
k3s server \
  '--token=<TOKEN>' \
  '--tls-san' \
  '<DOMAIN>' \
  '--cluster-init'
```

Once the server is confirmed healthy, stop this manual process (Ctrl+C) before proceeding.

### Step 5: Start K3s normally via systemd

```bash
systemctl start k3s
```

## Adjust Kubelet Resource Limits

Add the following kubelet arguments to the K3s service unit file at `/etc/systemd/system/k3s.service` to configure eviction thresholds:

```bash
ExecStart=/usr/local/bin/k3s \
    ... \
    '--kubelet-arg=eviction-hard=memory.available<500Mi,nodefs.available<10%' \
    '--kubelet-arg=eviction-soft=memory.available<1Gi,nodefs.available<15%' \
    '--kubelet-arg=eviction-soft-grace-period=memory.available=1m30s,nodefs.available=1m30s'
```

After editing the service file, reload systemd and restart K3s:

```bash
systemctl daemon-reload
systemctl restart k3s
```
