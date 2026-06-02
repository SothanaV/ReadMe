# Proxmox Cloud-Init VM Template

Create a reusable Ubuntu Cloud-Init VM template in Proxmox and clone it to provision new VMs quickly.

## Table of Contents

- [1. Download the Cloud-Init Image](#1-download-the-cloud-init-image)
- [2. Create the VM](#2-create-the-vm)
- [3. Import the Image to Storage](#3-import-the-image-to-storage)
- [4. Attach the Disk to the VM](#4-attach-the-disk-to-the-vm)
- [5. Add the Cloud-Init Drive](#5-add-the-cloud-init-drive)
- [6. Set the Boot Disk](#6-set-the-boot-disk)
- [7. Set the Serial Console](#7-set-the-serial-console)
- [8. Enable QEMU Guest Agent](#8-enable-qemu-guest-agent)
- [9. Configure Cloud-Init Settings](#9-configure-cloud-init-settings)
- [10. Convert to Template](#10-convert-to-template)
- [11. Clone and Provision](#11-clone-and-provision)

---

## 1. Download the Cloud-Init Image

Open a shell on the Proxmox host and download the Ubuntu Noble (24.04) cloud image:

```bash
cd /var/lib/vz/template/iso
wget https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img
```

> Image source: <https://cloud-images.ubuntu.com/noble/current/>

---

## 2. Create the VM

Create a new VM with ID `9000` (used as the template). Adjust memory and network bridge as needed:

```bash
qm create 9000 --memory 2048 --net0 virtio,bridge=vmbr0 --name ubuntu-cloudinit
```

---

## 3. Import the Image to Storage

Import the downloaded image as a disk into the `local-lvm` storage pool:

```bash
qm importdisk 9000 noble-server-cloudimg-amd64.img local-lvm
```

---

## 4. Attach the Disk to the VM

Attach the imported disk to the VM as a SCSI device:

```bash
qm set 9000 --scsihw virtio-scsi-pci --scsi0 local-lvm:vm-9000-disk-0
```

---

## 5. Add the Cloud-Init Drive

Add a Cloud-Init drive on the IDE bus. Proxmox will use this to pass configuration data to the VM on first boot:

```bash
qm set 9000 --ide2 local-lvm:cloudinit
```

---

## 6. Set the Boot Disk

Configure the VM to boot from the SCSI disk:

```bash
qm set 9000 --boot c --bootdisk scsi0
```

---

## 7. Set the Serial Console

Enable a serial console, which is required for Cloud-Init image display output:

```bash
qm set 9000 --serial0 socket --vga serial0
```

---

## 8. Enable QEMU Guest Agent

Recommended — allows Proxmox to interact with the guest OS (e.g., to get the IP address):

```bash
qm set 9000 --agent enabled=1
```

---

## 9. Configure Cloud-Init Settings

### Via the Proxmox Web GUI

Select VM `9000` and go to the **Cloud-Init** tab:

- **User**: enter your username (e.g. `sothana`)
- **Password**: set a login password
- **SSH Public Key**: paste your public key (required for automation)
- **IP Config**: set to DHCP or specify a static IP

Click **Regenerate Image** to write the settings to the Cloud-Init drive.

### Via CLI

```bash
qm set 9000 --ciuser sothana --cipassword yourpassword
qm set 9000 --sshkeys ~/.ssh/authorized_keys
qm set 9000 --ipconfig0 ip=dhcp
qm cloudinit update 9000
```

---

## 10. Convert to Template

### Convert via CLI

```bash
qm template 9000
```

### Convert via Web GUI

Right-click VM `9000` and select **Convert to Template**.

---

## 11. Clone and Provision

### Clone via CLI

```bash
qm clone 9000 <new-vm-id> --name <hostname> --full
```

### Clone via Web GUI

Right-click Template `9000` and select **Clone**. Choose **Full Clone** mode for best performance.

### Before starting the new VM

- Go to the **Cloud-Init** tab to update the hostname or IP address.
- Go to **Hardware** → **Hard Disk** → **Resize Disk** to expand storage (e.g. add 90 GB for a 100 GB total disk).

```bash
# Resize disk via CLI
qm resize <new-vm-id> scsi0 +90G
```

Click **Start**. Cloud-Init will automatically configure the VM on first boot.
