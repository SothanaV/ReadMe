# Linux create swap
- list swap
```bash
sudo swapon --show
```

- check space
```bash
df -h
```

- create swap
```bash
sudo fallocate -l 2G /swapfile
sudo dd if=/dev/zero of=/swapfile bs=1M count=2048
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

- check
```bash
sudo swapon --show
free -h
```