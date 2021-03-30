# map volume ec2 <> s3 bucket

-  install package
```
sudo apt install s3fs
```

-  set IAM Role with Full Access to S3 #aws
- install aws cli
```
apt install awscli
```
-  create/get user Full Access to S3 creadential
```
aws configure
# enter creadential
```

- create the Mountpoint 
```
mkdir -p <dir>
```

- create s3 bucket
```
aws s3 mb s3://<bucketname>
```
- edit /etc/fuse.conf
```
sudo nano /etc/fuse.conf
# un comment 
user_allow_other
```
- mount s3 file system
```
s3fs <bucketname> <dir> -o allow_other -o nonempty
```

# additional command

```
# unmount 
umount -l <path>
```