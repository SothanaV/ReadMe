# Settings Ubuntu Network command

- open config file at ```/etc/network/interfaces```

```bash
sudo nano /etc/network/interfaces
```

- edit like this
```bash
... 

auto ens18
iface ens18 inet static
  address 192.168.0.2
  netmask 255.255.255.0
  gateway 192.168.0.1
  dns-nameservers 89.207.128.252 89.207.130.252
...
```

- restart network config
```bash
sudo systemctl restart networking
```