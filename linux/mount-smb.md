# Mount SMB/CIFS Share on Linux

Mount a Windows or Samba network share on a Linux system using the CIFS protocol.

## Table of Contents

- [Install](#install)
- [Test the Connection](#test-the-connection)
- [Mount the Share](#mount-the-share)
- [Persistent Mount via fstab](#persistent-mount-via-fstab)

---

## Install

```bash
sudo apt update
sudo apt install cifs-utils
```

---

## Test the Connection

Use `smbclient` to verify access to the share before mounting:

```bash
smbclient //<host>/<share> -U <username>
```

Example with a domain user:

```bash
smbclient "//server.local/Data Lakehouse/Landing" -U myorg/SothanaV
```

Once connected, you can use `ls` to list files and `cd` to navigate directories.

---

## Mount the Share

Create a mount point directory, then mount the share:

```bash
# Create the mount point
sudo mkdir -p /mnt/data

# Mount the share
sudo mount -t cifs //server.local/Data /mnt/data -o username=SothanaV,domain=myorg
```

You will be prompted for the user's password. To pass it inline (less secure):

```bash
sudo mount -t cifs //server.local/Data /mnt/data \
  -o username=SothanaV,password=yourpassword,domain=myorg
```

---

## Persistent Mount via fstab

To mount the share automatically on boot, store credentials in a file and reference it in `/etc/fstab`.

### Create a credentials file

```bash
sudo nano /etc/samba/credentials
```

Add the following content:

```text
username=SothanaV
password=yourpassword
domain=myorg
```

Restrict access to the file:

```bash
sudo chmod 600 /etc/samba/credentials
```

### Add the fstab entry

```bash
sudo nano /etc/fstab
```

Append this line:

```text
//server.local/Data  /mnt/data  cifs  credentials=/etc/samba/credentials,iocharset=utf8  0  0
```

Apply without rebooting:

```bash
sudo mount -a
```
