# K3s etcd Backup and Restore

## Table of Contents

- [Backup to S3](#backup-to-s3)
- [Restore from S3](#restore-from-s3)

## Backup to S3

Run the following command on the K3s server node to take an etcd snapshot and upload it directly to an S3-compatible bucket:

```bash
k3s etcd-snapshot save \
  --s3 \
  --s3-bucket=<S3-BUCKET-NAME> \
  --s3-access-key=<S3-ACCESS-KEY> \
  --s3-secret-key=<S3-SECRET-KEY> \
  --s3-endpoint="storage.googleapis.com" \
  --etcd-s3-folder="etcd"
```

## Restore from S3

> **Warning:** This operation resets the cluster state. Perform this on the primary server node only, with the K3s service stopped.

### Step 1: Stop the K3s service

```bash
systemctl stop k3s
```

### Step 2: Run the cluster reset with snapshot restore

Replace `<SNAPSHOT-NAME>` with the exact snapshot file name stored in the S3 folder (e.g., `etcd-snapshot-2024-01-01T00:00:00Z`).

```bash
k3s server \
  --cluster-init \
  --cluster-reset \
  --etcd-s3 \
  --cluster-reset-restore-path=<SNAPSHOT-NAME> \
  --etcd-s3-bucket=<S3-BUCKET-NAME> \
  --etcd-s3-endpoint="storage.googleapis.com" \
  --etcd-s3-folder="etcd" \
  --etcd-s3-access-key=<S3-ACCESS-KEY> \
  --etcd-s3-secret-key=<S3-SECRET-KEY>
```

### Step 3: Start the K3s service normally

```bash
systemctl start k3s
```
