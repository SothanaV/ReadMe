# ClickHouse

## Manage Users, Roles, and Permissions

### Create a User

```sql
CREATE USER IF NOT EXISTS <username>
ON CLUSTER default
IDENTIFIED WITH plaintext_password BY '<password>';
```

### Create a Role

```sql
CREATE ROLE IF NOT EXISTS <role_name>
ON CLUSTER default;
```

### Grant Privileges to a Role

```sql
GRANT ON CLUSTER 'default'
    <privilege_name> ON <scope>
    TO <role_name> WITH GRANT OPTION;
```

### Grant a Role to a User

```sql
GRANT <role_name> TO <username>
ON CLUSTER default;
```

### Grant Table Access to a User

```sql
GRANT SELECT ON default.<table_name> TO <username>
ON CLUSTER default;
```

## Create a Replicated Table on a Cluster

The following statement creates a replicated table using the `ReplicatedMergeTree` engine, which enables data replication across cluster shards and replicas.

```sql
CREATE TABLE IF NOT EXISTS <table_name> ON CLUSTER default
(
    `<column_name>` <data_type>,
    ...
)
ENGINE = ReplicatedMergeTree(
    '/clickhouse/tables/{shard}/<table_name>',
    '{replica}'
)
PARTITION BY <partition_column>
ORDER BY <order_column>;
```

**Parameters:**

- `{shard}` and `{replica}` are macros automatically substituted by ClickHouse using the values defined in `config.xml` (or `macros.xml`) on each node.
- `PARTITION BY` — defines how data is split into partitions (e.g., by date or category).
- `ORDER BY` — defines the primary index and sort order within each partition.
