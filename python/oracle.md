# Query an Oracle Database from Python

## Table of Contents

- [Install Oracle Instant Client](#install-oracle-instant-client)
- [Example Usage](#example-usage)
- [Full Setup Script](#full-setup-script)

---

## Install Oracle Instant Client

Reference: [Oracle Instant Client Downloads for Linux x86-64](https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html)

### 1. Download

```bash
wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basic-linuxx64.zip
```

### 2. Unzip

```bash
unzip instantclient-basic-linuxx64.zip
```

### 3. Move to `/opt/oracle/`

```bash
sudo mkdir -p /opt/oracle
sudo mv instantclient_23_7 /opt/oracle/
```

### 4. Configure the Dynamic Linker

```bash
sudo sh -c "echo /opt/oracle/instantclient_23_7 > /etc/ld.so.conf.d/oracle-instantclient.conf"
sudo ldconfig
```

### 5. Install `libaio`

```bash
wget http://archive.ubuntu.com/ubuntu/pool/main/liba/libaio/libaio1_0.3.112-5_amd64.deb
sudo dpkg -i libaio1_0.3.112-5_amd64.deb
```

---

## Example Usage

```python
import cx_Oracle
import pandas as pd

dsn = "<HOST>:<PORT>/<SERVICE_NAME>"
user = "<USER>"
password = "<PASSWORD>"

connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)

df = pd.read_sql_query("""
    SELECT *
    FROM TABLE_NAME
""", connection)

print(df)
```

---

## Full Setup Script

Save as `config-oracle.sh` and run once on a fresh machine:

```bash
#!/bin/bash
sudo apt update
sudo apt install -y gcc unzip wget git

sudo mkdir -p /opt/oracle
cd /opt/oracle

sudo wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basic-linuxx64.zip
sudo unzip instantclient-basic-linuxx64.zip

sudo sh -c "echo /opt/oracle/instantclient_23_6 > /etc/ld.so.conf.d/oracle-instantclient.conf"
sudo ldconfig

sudo wget http://archive.ubuntu.com/ubuntu/pool/main/liba/libaio/libaio1_0.3.112-5_amd64.deb
sudo dpkg -i libaio1_0.3.112-5_amd64.deb
```
