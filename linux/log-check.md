# Log and Service Inspection

## Table of Contents

- [journalctl — systemd Journal Logs](#journalctl--systemd-journal-logs)
- [supervisorctl — Supervisor Process Manager](#supervisorctl--supervisor-process-manager)
- [systemctl — Service Management](#systemctl--service-management)

---

## journalctl — systemd Journal Logs

Follow live logs for a specific service:

```bash
journalctl -xefu <service-name>.service
```

The `.service` suffix is optional:

```bash
journalctl -xefu <service-name>
```

**Common flags:**

| Flag | Description                                      |
|------|--------------------------------------------------|
| `-x` | Add explanatory help text to log entries         |
| `-e` | Jump to the end of the journal                   |
| `-f` | Follow new log entries in real time              |
| `-u` | Filter by a specific unit (service)              |

Show logs from the last boot:

```bash
journalctl -b
```

Show logs for a specific time range:

```bash
journalctl --since "2024-01-01 00:00:00" --until "2024-01-02 00:00:00"
```

---

## supervisorctl — Supervisor Process Manager

Check the status of all supervised processes:

```bash
sudo supervisorctl status
```

Other useful commands:

```bash
sudo supervisorctl start <program>      # Start a program
sudo supervisorctl stop <program>       # Stop a program
sudo supervisorctl restart <program>    # Restart a program
sudo supervisorctl tail -f <program>    # Follow the program's log output
```

---

## systemctl — Service Management

List all active services:

```bash
systemctl list-units --type=service
```

Other useful commands:

```bash
sudo systemctl status <service>     # Show service status
sudo systemctl start <service>      # Start a service
sudo systemctl stop <service>       # Stop a service
sudo systemctl restart <service>    # Restart a service
sudo systemctl enable <service>     # Enable service to start on boot
sudo systemctl disable <service>    # Disable service from starting on boot
```
