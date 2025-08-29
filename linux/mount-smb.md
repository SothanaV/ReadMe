# Mount smb protocol to linux

- install 
```
apt update 
apt install cifs-utils
```

- test

```
smbclient <host> -U user

eg smbclient "server.local/Data Lakehouse/Landing" -U myorg/SothanaV
```

it can `ls` and `cd`

- mount
```
# create mount dir
mkdir -p /mnt/data
sudo mount -t cifs //server.local/Data /mnt/data  -o username=SothanaV,domain=myorg
```