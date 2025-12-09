# Clickhouse
## Manage user, role, permission
- create user
```sql
CREATE USER IF NOT EXISTS <username> 
ON CLUSTER default
IDENTIFIED WITH plaintext_password BY '<PASSWORD>'
```

- create role
```sql
CREATE ROLE IF NOT EXISTS <role_name> 
ON CLUSTER default
```

- grant privilege to role
```sql
GRANT ON CLUSTER 'default'
<privilege_name> ON <scope> 
TO <role_name> WITH GRANT OPTION
```

- grant role to user
```sql
GRANT <role_name> TO <username>
ON CLUSTER default
```

- grant table to user
```sql
GRANT SELECT ON default.<table_name> TO <username> 
ON CLUSTER default
```

## create table on cluster
- create table
```
CREATE TABLE IF NOT EXISTS <tablename> ON CLUSTER default
(
    `<column_name>` <data_type>,
    ...
)
ENGINE = ReplicatedMergeTree(
    '/clickhouse/tables/{shard}/<tablename>',
    '{replica}'
)
PARTITION BY <partition_column>
ORDER BY <order_column>
```