# k3s-backup-etcd

## backup
```
k3s etcd-snapshot \
  --s3 \
  --s3-bucket=ditp-backup\
  --s3-access-key=<S3-ACCESS-KEY> \
  --s3-secret-key=<S3-SECRET-KEY> \
  --s3-endpoint="storage.googleapis.com" \
  --etcd-s3-folder="etcd"
```

## restore
- stop k3s server
- run command
```
k3s server \
  --cluster-init \
  --cluster-reset \
  --etcd-s3 \
  --cluster-reset-restore-path=<SNAPSHOT-NAME> \
  --etcd-s3-bucket=<S3-BUCKET-NAME> \
  --etcd-s3-endpoint="storage.googleapis.com" \
  --etcd-s3-folder="etcd" \
  --etcd-s3-access-key=<S3-ACCESS-KEY> \
  --etcd-s3-secret-key=<S3-SECRET-KEY>
```


