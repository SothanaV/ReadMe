# VM Proxy Setup Guide

Route a host machine's `apt` traffic through a Virtual Machine (VM) that has internet access, bypassing a host-level firewall.

## Table of Contents

- [Option A: Tinyproxy (HTTP Proxy)](#option-a-tinyproxy-http-proxy)
  - [1. On the VM (Gateway)](#1-on-the-vm-gateway)
  - [2. On the Host (Client)](#2-on-the-host-client)
  - [Usage and Troubleshooting](#usage-and-troubleshooting)
- [Option B: SSH SOCKS Tunnel (Quickest)](#option-b-ssh-socks-tunnel-quickest)

---

## Option A: Tinyproxy (HTTP Proxy)

### 1. On the VM (Gateway)

Install and configure `tinyproxy` to act as the proxy server.

#### Install Tinyproxy

```bash
sudo apt update && sudo apt install tinyproxy -y
```

#### Configure Access

Edit the Tinyproxy configuration file:

```bash
sudo nano /etc/tinyproxy/tinyproxy.conf
```

Find the **Allow** section and add the host machine's IP address:

```text
Allow 127.0.0.1
Allow <HOST_IP>
```

#### Restart the Service

```bash
sudo systemctl restart tinyproxy
```

Allow the proxy port through the firewall:

```bash
sudo ufw allow 8888
```

---

### 2. On the Host (Client)

Configure `apt` to route traffic through the VM proxy.

#### Create the apt Proxy Config File

```bash
sudo nano /etc/apt/apt.conf.d/99proxy
```

#### Add Proxy Settings

Replace `<VM_IP>` with the actual IP address of the VM:

```text
Acquire::http::Proxy "http://<VM_IP>:8888/";
Acquire::https::Proxy "http://<VM_IP>:8888/";
```

---

### Usage and Troubleshooting

- **Update packages:** Run `sudo apt update` as normal; traffic is routed through the VM.
- **Disable the proxy:** Comment out the lines in `/etc/apt/apt.conf.d/99proxy` with `#` when the VM is off.
- **Check connectivity:** Ensure port `8888` is open on the VM with `sudo ufw allow 8888`.
- **Check Tinyproxy logs:** `sudo journalctl -u tinyproxy -f`

---

## Option B: SSH SOCKS Tunnel (Quickest)

No additional software required on the VM — only an SSH server.

**Step 1:** From the host machine, open an SSH SOCKS5 tunnel to the VM (keep this terminal open):

```bash
ssh -D 1080 <user>@<vm-ip>
```

**Step 2:** On the host, run `apt` through the SOCKS5 tunnel:

```bash
sudo apt -o Acquire::http::Proxy="socks5h://127.0.0.1:1080/" update
```

> `socks5h` means DNS resolution is also done through the tunnel, which avoids DNS leaks.
