# Network config using netplan
ref https://netplan.readthedocs.io/en/latest/netplan-yaml/

- edit config
```bash
sudo nano /etc/netplan/00-installer-config.yaml
```

```
network:
  ethernets:
    ens35:
      addresses:
        - 10.16.4.21x/24
    ens36:
      addresses:
        - 10.16.5.21x/24
  version: 2
```

- apply
```bash
sudo netplan apply
```