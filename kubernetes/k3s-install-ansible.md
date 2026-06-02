# K3s Installation Using Ansible

## Prerequisites

- Python 3 installed on the control machine
- SSH access via key-based authentication to all target nodes ([ssh-key-gen guide](/linux/ssh-key-gen.md))
- A user with root (sudo) permissions on all target nodes

## Table of Contents

- [Step 0: Install Ansible](#step-0-install-ansible)
- [Step 1: Clone the K3s Ansible Repository](#step-1-clone-the-k3s-ansible-repository)
- [Step 2: Configure the Inventory](#step-2-configure-the-inventory)
- [Step 3: Run the Playbook](#step-3-run-the-playbook)

## Step 0: Install Ansible

Create a Python virtual environment and install Ansible:

```bash
python3 -m venv env
source env/bin/activate
pip install ansible
```

## Step 1: Clone the K3s Ansible Repository

```bash
git clone https://github.com/k3s-io/k3s-ansible.git
cd k3s-ansible
```

## Step 2: Configure the Inventory

Copy the sample inventory and generate a secure token:

```bash
cp inventory-sample.yml inventory.yml

# Generate a random cluster token
openssl rand -base64 64
```

Edit `inventory.yml` with your node IPs, credentials, and the generated token:

```yaml
---
k3s_cluster:
  children:
    server:
      hosts:
        10.16.2.33:
        10.16.2.34:
        10.16.2.35:
    agent:
      hosts:
        10.16.2.31:
        10.16.2.32:

  vars:
    ansible_port: 22
    ansible_user: admin
    ansible_ssh_private_key_file: <key_path>
    k3s_version: v1.34.1+k3s1
    token: "<TOKEN>"
    api_endpoint: "{{ hostvars[groups['server'][0]]['ansible_host'] | default(groups['server'][0]) }}"
```

## Step 3: Run the Playbook

### Install

```bash
ansible-playbook playbooks/site.yml -i inventory.yml
```

### Upgrade

```bash
ansible-playbook playbooks/upgrade.yml -i inventory.yml
```
