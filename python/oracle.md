# Setup python query oracle database
- download oracle instantclient
    - ref [oracle instant-client](https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html)
```
wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basic-linuxx64.zip
```

- unzip
```
unzip instantclient-basic-linuxx64.zip
```
- move to `/opt/oracle/`
```
sudo mkdir -p /opt/oracle
sudo mv instantclient-basic-linuxx64.zip /opt/oracle/
```

- install `libaio`
```
wget http://archive.ubuntu.com/ubuntu/pool/main/liba/libaio/libaio1_0.3.112-5_amd64.deb
sudo dpkg -i libaio1_0.3.112-5_amd64.deb
```

## Example usage
```py
import cx_Oracle
import pandas as pd

dsn = "<HOST>:<PORT>/<SERVICE_NAME>"
user = "<USER>"
password = "<PASSWORD>"
connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)

df = pd.read_sql_query("""
SELECT
    *
FROM
   TABLE
""", connection)
print(df)
```