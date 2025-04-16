# Airflow command
- list dags run list

```
airflow dags list-runs --no-backfill --dag-id <DAG_ID> --start-date <START_DATE> --end-date <END_DATE> | grep fail

# eg
## airflow dags list-runs --no-backfill --dag-id fact_mms_transaction --start-date 2025-04-10 --end-date 2025-04-16 | grep fail
```

- clear failed dags run
```
airflow tasks clear fact_mms_transaction --start-date 2025-04-10 --end-date 2025-04-16 --only-failed

# eg
## airflow tasks clear <DAG_ID> --start-date <START_DATE> --end-date <END_DATE> --only-failed
```