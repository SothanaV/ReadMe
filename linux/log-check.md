# journalctl
- display services logs
```bash
journalctl -xefu service-name.service
```

or

```
journalctl -xefu service-name
```

# supervisorctl
```bash
sudo supervisorctl status
```

# systemctl
```bash
systemctl list-units --type=service
```