# Create a Swap File on Linux

Add a swap file to a Linux system that has no swap space, or to increase existing swap.

## Table of Contents

- [Check Existing Swap](#check-existing-swap)
- [Check Available Disk Space](#check-available-disk-space)
- [Create the Swap File](#create-the-swap-file)
- [Verify](#verify)
- [Remove Swap (Optional)](#remove-swap-optional)

---

## Check Existing Swap

```bash
sudo swapon --show
```

If the output is empty, no swap is currently active.

---

## Check Available Disk Space

Ensure the filesystem has enough space for the swap file:

```bash
df -h
```

---

## Create the Swap File

The steps below create a 2 GB swap file. Adjust the size as needed.

```bash
# Allocate the file (fast, uses fallocate)
sudo fallocate -l 2G /swapfile

# Alternative if fallocate is not supported by your filesystem (e.g., Btrfs)
sudo dd if=/dev/zero of=/swapfile bs=1M count=2048

# Restrict permissions so only root can read/write it
sudo chmod 600 /swapfile

# Format it as swap space
sudo mkswap /swapfile

# Activate the swap file
sudo swapon /swapfile

# Make the swap file persist across reboots
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## Verify

```bash
sudo swapon --show
free -h
```

---

## Remove Swap (Optional)

To disable and delete the swap file:

```bash
sudo swapoff /swapfile
sudo rm /swapfile
```

Then remove the `/swapfile` line from `/etc/fstab`.
