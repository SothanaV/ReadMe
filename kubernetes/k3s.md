# K3S

### restore etcd from snapshort
1. stop k3s service
```bash
systemctl stop k3s
```
2. find desired snapshort at `/var/lib/rancher/k3s/server/db/snapshots`
3. restore etcd from snapshort
```bash
k3s server \
  --cluster-reset \
  --cluster-reset-restore-path=/var/lib/rancher/k3s/server/db/snapshots/<SNAPSHORT_PATH_FROM2> \
  --etcd-arg=quota-backend-bytes=$((8*1024*1024*1024))
```
4. try to start k3s command find from 
  - cat command to run k3s
  ```bash
  cat /etc/systemd/system/k3s.service
  ```
  - start k3 monitor logs
  ```bash
  k3s server \
    '--token=<TOKEN>' \
    '--tls-san' \
    '<DOMAIN>' \
    '--cluster-init' 
  ```

5. stop step4 and start normal k3s
```
system start k3s
```