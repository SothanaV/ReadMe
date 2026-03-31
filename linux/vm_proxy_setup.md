# VM Proxy Setup Guide

This guide explains how to bypass a host-level firewall by routing the host's `apt` traffic through a Virtual Machine (VM) that has internet access.

---

## 1. On the Virtual Machine (The Gateway)
Install and configure `tinyproxy` to act as the middleman.

### Install Tinyproxy
```bash
sudo apt update && sudo apt install tinyproxy -y
```

### Configure Access
Edit `/etc/tinyproxy/tinyproxy.conf`:
```bash
sudo nano /etc/tinyproxy/tinyproxy.conf
```
Find the **Allow** section and add your laptop's IP:
```text
Allow 127.0.0.1
Allow [YOUR_LAPTOP_IP]
```

### Restart Service
```bash
sudo systemctl restart tinyproxy
```

---

## 2. On the Laptop (The Client)
Configure `apt` to use the VM as a proxy.

### Create Config File
```bash
sudo nano /etc/apt/apt.conf.d/99proxy
```

### Add Proxy Settings
Replace `[VM_IP]` with the actual IP address of your VM:
```text
Acquire::http::Proxy "http://[VM_IP]:8888/";
Acquire::https::Proxy "http://[VM_IP]:8888/";
```

---

## 3. Usage & Troubleshooting
- **To Update:** Run `sudo apt update`.
- **To Disable:** If the VM is off, comment out the lines in `/etc/apt/apt.conf.d/99proxy` using `#`.
- **Check Ports:** Ensure the VM allows traffic on port **8888** (`sudo ufw allow 8888`).
