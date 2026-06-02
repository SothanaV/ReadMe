# Expand Disk on Linux

Grow a partition and resize the filesystem after expanding a virtual or physical disk.

## Table of Contents

- [Standard Partition (ext4)](#standard-partition-ext4)
- [Logical Volume (LVM)](#logical-volume-lvm)

---

## Standard Partition (ext4)

### Step 1: Grow the Partition

Use `growpart` to expand the partition to fill the available disk space:

```bash
growpart <disk> <partition-number>

# Example: expand partition 1 on /dev/sda
growpart /dev/sda 1
```

### Step 2: Stop Services Using the Disk

Stop any services that have open files on the filesystem before resizing (if resizing offline):

```bash
sudo systemctl stop <service-name>
```

### Step 3: Resize the Filesystem

Resize the ext4 filesystem to fill the expanded partition:

```bash
resize2fs <partition>

# Example:
resize2fs /dev/sda1
```

> `resize2fs` supports online resizing for ext4 — the filesystem does not need to be unmounted in most cases.

---

## Logical Volume (LVM)

Use this path when the disk is managed by LVM (common on Ubuntu server installs).

### Step 1: Resize the Physical Volume

After expanding the underlying disk or partition, inform LVM of the new size:

```bash
sudo pvresize <partition>

# Example:
sudo pvresize /dev/sda3
```

### Step 2: Extend the Logical Volume

Extend the logical volume to use all available free space in the volume group:

```bash
sudo lvextend -l +100%FREE <logical-volume>

# Example:
sudo lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv
```

### Step 3: Resize the Filesystem

Resize the filesystem on the logical volume:

```bash
sudo resize2fs <logical-volume>

# Example:
sudo resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv
```

Verify the new size:

```bash
df -h
```
