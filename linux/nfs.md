# NFS on Ubuntu

Set up an NFS server and mount shares on a client.

## Table of Contents

- [Server Setup](#server-setup)
- [Client Setup](#client-setup)

---

## Server Setup

### Step 1: Update System Packages

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2: Install the NFS Server Package

```bash
sudo apt install nfs-kernel-server -y
```

### Step 3: Create a Directory for Sharing

```bash
sudo mkdir -p /srv/nfs/share
sudo chown nobody:nogroup /srv/nfs/share
sudo chmod 777 /srv/nfs/share
```

### Step 4: Configure Exports

Open the exports file:

```bash
sudo nano /etc/exports
```

Add an export entry. Replace `192.168.1.0/24` with your network range, or use `*` to allow any IP:

```text
/srv/nfs/share 192.168.1.0/24(rw,sync,no_subtree_check)
```

**Common export options:**

| Option              | Description                                              |
|---------------------|----------------------------------------------------------|
| `rw`                | Allow read and write access                              |
| `ro`                | Allow read-only access                                   |
| `sync`              | Write changes to disk before replying to client          |
| `no_subtree_check`  | Disable subtree checking (improves reliability)          |
| `no_root_squash`    | Allow root on the client to act as root on the server    |

### Step 5: Apply Export Configuration

```bash
sudo exportfs -a
```

### Step 6: Restart the NFS Service

```bash
sudo systemctl restart nfs-kernel-server
```

### Step 7: Allow NFS Through the Firewall

```bash
sudo ufw allow from 192.168.1.0/24 to any port nfs
sudo ufw reload
```

### Step 8: Verify NFS Exports

```bash
sudo exportfs -v
```

---

## Client Setup

### Verify Export Availability

Use `showmount` to list the shares exported by the server:

```bash
showmount -e 192.168.28.91
```

### Mount the Share

```bash
mkdir ~/nfs_test
sudo mount -t nfs 192.168.28.91:/srv/nfs/share ~/nfs_test
```

### Persistent Mount via fstab

To mount the share automatically on boot, add an entry to `/etc/fstab`:

```bash
sudo nano /etc/fstab
```

Append:

```text
192.168.28.91:/srv/nfs/share  /mnt/nfs_share  nfs  defaults  0  0
```

Apply without rebooting:

```bash
sudo mount -a
```
