# Mount an S3 Bucket on EC2 Using s3fs

s3fs allows you to mount an Amazon S3 bucket as a local filesystem on Linux using FUSE.

## Prerequisites

- An AWS account with an IAM user or IAM role that has S3 access
- An EC2 instance running Ubuntu/Debian

## Steps

### 1. Install s3fs and AWS CLI

```bash
sudo apt install s3fs awscli
```

### 2. Configure AWS Credentials

If using an IAM role attached to the EC2 instance, credentials are provided automatically and this step can be skipped. Otherwise, configure credentials for an IAM user with S3 full access:

```bash
aws configure
```

Enter your Access Key ID, Secret Access Key, default region, and output format when prompted.

### 3. Create the S3 Bucket

```bash
aws s3 mb s3://<bucket-name> --region ap-southeast-1
```

Replace `<bucket-name>` with your desired bucket name and adjust the region as needed.

### 4. Create the Mount Directory

```bash
mkdir -p /mnt/<dir>
```

### 5. Allow Other Users to Access the FUSE Mount

Edit `/etc/fuse.conf` and uncomment the `user_allow_other` line:

```bash
sudo nano /etc/fuse.conf
```

Uncomment the following line:

```
user_allow_other
```

### 6. Mount the S3 Bucket

```bash
s3fs <bucket-name> /mnt/<dir> \
  -o allow_other \
  -o nonempty \
  -o use_path_request_style \
  -o url=https://s3-<aws-region>.amazonaws.com
```

Replace `<bucket-name>`, `/mnt/<dir>`, and `<aws-region>` with your actual values.

## Additional Commands

### Unmount the Bucket

```bash
umount -l /mnt/<dir>
```

## Notes

- For persistent mounts across reboots, add the mount command to `/etc/fstab` or a systemd unit.
- IAM role-based authentication on EC2 is preferred over static credentials for security.
