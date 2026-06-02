# Ansible

## Overview

Ansible is an open-source automation tool for configuration management, application deployment, and task automation.

## Installation

### Install via pip

```bash
pip install ansible
```

### Install via apt (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install ansible -y
```

### Verify Installation

```bash
ansible --version
```

## Basic Usage

### Run an Ad-hoc Command

```bash
ansible all -i inventory.ini -m ping
ansible all -i inventory.ini -m shell -a "uptime"
```

### Run a Playbook

```bash
ansible-playbook -i inventory.ini playbook.yml
```

### Run with a Specific User

```bash
ansible-playbook -i inventory.ini playbook.yml -u <remote-user> --ask-become-pass
```

## Inventory File Example

```ini
[webservers]
192.168.1.10
192.168.1.11

[dbservers]
192.168.1.20
```

## Playbook Example

```yaml
---
- name: Install and start nginx
  hosts: webservers
  become: true

  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Start nginx service
      service:
        name: nginx
        state: started
        enabled: yes
```

## References

- [Ansible Official Documentation](https://docs.ansible.com/)
- [Ansible Galaxy](https://galaxy.ansible.com/)
