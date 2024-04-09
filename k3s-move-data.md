# K3S move data

master
```
systemctl status k3s

systemctl stop k3s

/usr/local/bin/k3s-killall.sh

systemctl start k3s

systemctl status k3s
```

agent
```bash
systemctl status k3s-agent

systemctl stop k3s-agent

/usr/local/bin/k3s-killall.sh

systemctl start k3s-agent

systemctl status k3s-agent
```

### move data and symlink

```bash
#/bin/bash
# ref : https://mrkandreev.name/snippets/how_to_move_k3s_data_to_another_location/
mv /run/k3s/ /mnt/data_store/k3s/
mv /var/lib/kubelet/pods/ /mnt/data_store/k3s-pods/
mv /var/lib/rancher/ /mnt/data_store/k3s-rancher/

ln -s /mnt/data_store/k3s/ /run/k3s
ln -s /mnt/data_store/k3s-pods/ /var/lib/kubelet/pods
ln -s /mnt/data_store/k3s-rancher/ /var/lib/rancher
```