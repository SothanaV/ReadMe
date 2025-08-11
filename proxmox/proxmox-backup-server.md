# Setup Proxmox Server
1. install proxmox backup server
2. add s3 endpint
3. add data store

1.	Install Proxmox Backup Server
	-	Either on a separate machine or as a VM/LXC inside your cluster.
	-	PBS Installation Guide
2.	Create an S3 Datastore in PBS
In PBS UI:
	-	Administration → Datastore → Add → S3
	-	Fill in:
	-	Name (e.g., s3-backup)
	-	Bucket Name
	-	Endpoint (e.g., https://s3.amazonaws.com or MinIO URL)
	-	Region
	-	Access Key / Secret Key
3.	Connect Proxmox VE to PBS
In Proxmox UI:
	-	Datacenter → Storage → Add → Proxmox Backup Server
	-	Enter the PBS hostname/IP, fingerprint, datastore name, and credentials.
4.	Run Backup
	-	Select your VM → Backup → Storage = PBS datastore
	-	Set schedule if needed (Datacenter → Backup Jobs).

# How to restore
1.	In Proxmox VE, go to:
Datacenter → Storage and make sure your PBS storage is already added.
(Uses PBS hostname/IP, datastore name, and fingerprint.)
2.	Go to:
Datacenter → Backups or VM → Backup tab.
3.	Select the backup entry you want (type .pxar for CT, .vma.zst for VMs).
4.	Click Restore.
	-	VM ID: Keep same ID or pick a new one.
	-	Target Node: The PVE node to restore to.
	-	Storage: Target storage (local-lvm, zfs, ceph, etc.).
	-	Options:
	-	Overwrite existing VM if restoring over an existing one.
	-	Start after restore if you want it to boot immediately.
5.	Click Restore and wait for completion.

# How to get fingerprint
On the PBS server, run:
```
proxmox-backup-client status --repository root@pam@localhost:datastore-name
```

When connecting for the first time, it will display something like:
```
Fingerprint: 12:34:56:78:90:AB:CD:EF:12:34:56:78:90:AB:CD:EF:12:34:56:78
```