# NSF on Ubuntu
## Ser
- Step 1: Update System Packages
```
sudo apt update && sudo apt upgrade -y
```

- Step 2: Install the NFS Server Package
```
sudo apt install nfs-kernel-server -y
```

- Step 3: Create a Directory for Sharing
```
sudo mkdir -p /srv/nfs/share
sudo chown nobody:nogroup /srv/nfs/share
sudo chmod 777 /srv/nfs/share
```

- Step 4: Configure Exports

    ```bash
    sudo nano /etc/exports
    ```

    - add config
        - Replace 192.168.1.0/24 with your network range or * for any IP.
    ```bash
    /srv/nfs/share 192.168.1.0/24(rw,sync,no_subtree_check)
    ```

- Step 5: Apply Export Configuration
```
sudo exportfs -a
```

- Step 6: Restart NFS Service
```
sudo systemctl restart nfs-kernel-server
```

- Step 7: Allow NFS Through the Firewall
```
sudo ufw allow from 192.168.1.0/24 to any port nfs
sudo ufw reload
```

- Step 8: Verify NFS Server
```
sudo exportfs -v
```

# client
- Use showmount to Verify Export Availability
```
showmount -e 192.168.28.91
```

- create directory and mount
```
mkdir ~/nfs_test
sudo mount -t nfs 192.168.28.91:/srv/nfs/share ~/nfs_test
```