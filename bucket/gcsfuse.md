# GCSFuse

GCSFuse allows you to mount a Google Cloud Storage bucket as a local filesystem on Linux.

## Install GCSFuse

Add the GCSFuse package repository and install the package:

```bash
export GCSFUSE_REPO=gcsfuse-$(lsb_release -c -s)
echo "deb [signed-by=/usr/share/keyrings/cloud.google.asc] https://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo tee /usr/share/keyrings/cloud.google.asc
sudo apt-get update
sudo apt-get install gcsfuse
```

## Mount a Bucket

Set the path to a service account key file and create the mount directory, then mount the bucket:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/home/serveradmin/dsm-data-platform-114e64663484.json
mkdir -p /var/lib/bucket

gcsfuse -o allow_other --dir-mode 777 --file-mode 777 dsm-data-platform /var/lib/bucket
```

Replace `dsm-data-platform` with your bucket name and `/var/lib/bucket` with your preferred mount path.

## Unmount the Bucket

```bash
fusermount -u /var/lib/bucket
```

## Map Longhorn Storage to a GCS Bucket

Create a per-node subdirectory inside the bucket mount and symlink the Longhorn data directory to it:

```bash
mkdir -p /var/lib/bucket/longhorn/$(hostname)
ln -rs /var/lib/bucket/longhorn/$(hostname)/ /var/lib/longhorn
```

## Optional: Migrate Existing Longhorn Data to the Bucket

Use `rsync` to safely transfer existing Longhorn data into the bucket-backed directory.

Perform a dry run first to preview what will be transferred:

```bash
rsync --verbose --archive --dry-run /var/lib/longhorn/ /var/lib/bucket/longhorn/$(hostname)
```

Run the actual transfer and remove source files after a successful copy:

```bash
rsync --verbose --archive --remove-source-files /var/lib/longhorn/ /var/lib/bucket/longhorn/$(hostname)
```

Or move the directory directly if the bucket is already mounted:

```bash
mv /var/lib/longhorn/ /var/lib/bucket/longhorn/$(hostname)
```
