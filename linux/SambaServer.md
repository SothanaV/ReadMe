# Samba Server

Share files from a Linux server over the network using the SMB protocol.
แชร์ไฟล์จาก Linux ผ่านโปรโตคอล SMB

## Table of Contents

- [Install](#install)
- [Edit Configuration](#edit-configuration)
- [Restart Services](#restart-services)
- [Set a Samba Password](#set-a-samba-password)

---

## Install

```bash
sudo apt install samba
```

---

## Edit Configuration

Navigate to the Samba configuration directory and open the config file:

```bash
cd /etc/samba/
sudo nano smb.conf
```

Add a share definition at the bottom of the file. Replace `YourPath` with the actual directory you want to share:

```ini
[share]
    comment = Ubuntu File Server Share
    path = /path/to/your/shared/folder
    browsable = yes
    guest ok = yes
    read only = no
    create mask = 0755
```

**Configuration options explained:**

| Option        | Description                                           |
|---------------|-------------------------------------------------------|
| `browsable`   | Whether the share appears when browsing the network   |
| `guest ok`    | Allow access without a Samba password                 |
| `read only`   | Set to `no` to allow write access                     |
| `create mask` | Default permissions for newly created files           |

---

## Restart Services

Apply the new configuration by restarting both Samba daemons:

```bash
sudo systemctl restart smbd.service nmbd.service
```

Verify the services are running:

```bash
sudo systemctl status smbd
sudo systemctl status nmbd
```

---

## Set a Samba Password

If `guest ok = no`, users must authenticate. Set a Samba password for a Linux user:

```bash
sudo smbpasswd -a <username>
```
