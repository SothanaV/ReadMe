# Proxmox Cloud-Init VM Template

## 1. Download Cloud-Init Image

Go to Proxmox shell:

```bash
cd /var/lib/vz/template/iso
wget https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img
```

> Image source: https://cloud-images.ubuntu.com/noble/current/

## 2. Create VM

```bash
qm create 9000 --memory 2048 --net0 virtio,bridge=vmbr0 --name ubuntu-cloudinit
```

## 3. Import Image to Storage

```bash
qm importdisk 9000 noble-server-cloudimg-amd64.img local-lvm
```

## 4. Attach Disk to VM as SCSI

```bash
qm set 9000 --scsihw virtio-scsi-pci --scsi0 local-lvm:vm-9000-disk-0
```

## 5. Add Cloud-Init Drive

```bash
qm set 9000 --ide2 local-lvm:cloudinit
```

## 6. Set Boot Disk

```bash
qm set 9000 --boot c --bootdisk scsi0
```

## 7. Set Serial Console

```bash
qm set 9000 --serial0 socket --vga serial0
```

## 8. Enable QEMU Guest Agent (Optional but Recommended)

```bash
qm set 9000 --agent enabled=1
```

## 9. Configure Cloud-Init via Web GUI

After running the commands above, go back to the Proxmox Web GUI:

- Select VM ID `9000` → go to the **Cloud-Init** tab
- **User**: enter your username (e.g. `sothana`)
- **Password**: set a password
- **SSH Public Key**: paste your public key here (important for automation)
- **IP Config**: set to DHCP or specify a static IP
- Click **Regenerate Image** to save the settings to the Cloud-Init drive

Or configure via CLI:

```bash
qm set 9000 --ciuser sothana --cipassword yourpassword
qm set 9000 --sshkeys ~/.ssh/authorized_keys
qm set 9000 --ipconfig0 ip=dhcp
qm cloudinit update 9000
```

## 10. Convert to Template

```bash
qm template 9000
```

Or via Web GUI:
- Right-click VM `9000` → select **Convert to Template**

## 11. Provisioning — Clone and Use

**Via CLI:**

```bash
qm clone 9000 <new-vm-id> --name <hostname> --full
```

**Via Web GUI:**
- Right-click Template `9000` → **Clone**
- Select **Full Clone** mode (recommended for performance)

**Before starting the VM:**
- Go to the **Cloud-Init** tab of the new VM to change the hostname or IP
- Go to **Hardware** → **Hard Disk** → **Resize Disk** to expand storage as needed (e.g. 100 GB for hot storage)

```bash
# Resize disk via CLI
qm resize <new-vm-id> scsi0 +90G
```

Click **Start** — Cloud-Init will automatically configure everything on first boot.
