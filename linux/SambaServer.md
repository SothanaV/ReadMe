# SAMBA_SERVER
share file on linux
แชร์ไฟล์จาก linux
## Install
	$ sudo apt install samba

## Edit config
	$ cd /etc/samba/
	$ sudo nano smb.conf

### Edit in nano
	[share]
    		comment = Ubuntu File Server Share
    		path = YourPart
    		browsable = yes
    		guest ok = yes
    		read only = no
    		create mask = 0755
## restart services
	$ sudo systemctl restart smbd.service nmbd.service