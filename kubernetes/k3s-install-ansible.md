# K3S install using ansible
required 
- python
- ssh via key [ssh-key-gen.md](/linux/ssh-key-gen.md)
- user as root permission


0. install ansible
```
python3 -m venv env
source env/bin/activate
pip install ansible
```

1. clone repo
```
git clone https://github.com/k3s-io/k3s-ansible.git
cd k3s-ansible
```

2. edit `inventory.yml`
```bash
cp inventory-sample.yml inventory.yml

# create token
openssl rand -base64 64

```

- edit
```yml
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

  # Required Vars
  vars:
    ansible_port: 22
    ansible_user: admin
    ansible_ssh_private_key_file: <key_path>
    k3s_version: v1.34.1+k3s1
    token: "<TOKEN>"
    api_endpoint: "{{ hostvars[groups['server'][0]]['ansible_host'] | default(groups['server'][0]) }}"
```

3. install
- install
    ```
    ansible-playbook playbooks/site.yml -i inventory.yml
    ```
- upgrade
    ```
    ansible-playbook playbooks/upgrade.yml -i inventory.yml
    ```