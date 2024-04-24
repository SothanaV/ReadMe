# GCSFUSE
## Config gcsfuse
### install gcsfuse
```bash
export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
echo "deb [signed-by=/usr/share/keyrings/cloud.google.asc] https://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo tee /usr/share/keyrings/cloud.google.asc
apt-get update
apt-get install gcsfuse
```

### config mount gcsfuse to local path
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/home/serveradmin/dsm-data-platform-114e64663484.json
mkdir /var/lib/bucket

gcsfuse -o allow_other --dir-mode 777 --file-mode 777 dsm-data-platform /var/lib/bucket
```


# map longhorn to nfs gcs
```bash
mkdir /var/lib/bucket/longhorn/$(hostname)
ln -rs /var/lib/bucket/longhorn/$(hostname)/ /var/lib/longhorn
```

### unmount 
```
fusermount -u /mnt/google-bucket
```


### optional
```bash
mv /var/lib/longhorn/ /mnt/google-bucket/longhorn/$(hostname)
rsync --verbose --archive --dry-run /var/lib/longhorn/ /mnt/google-bucket/longhorn/$(hostname)
rsync --verbose --archive --remove-source-files /var/lib/longhorn/ /mnt/google-bucket/longhorn/$(hostname)
```