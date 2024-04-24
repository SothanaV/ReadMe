# K3S

### restore etcd from snapshort
```
k3s server \
  --cluster-reset \
  --cluster-reset-restore-path=/var/lib/rancher/k3s/server/db/snapshots/etcd-snapshot-ssk001vm801-1712664000 \
  --etcd-arg=quota-backend-bytes=$((8*1024*1024*1024))

k3s server \
        '--token=qnvljsbv1uo' \
        '--tls-san' \
        'rancher.sec.dataforthai.org' \
        '--cluster-init' 
```