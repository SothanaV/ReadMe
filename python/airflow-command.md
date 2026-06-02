# Airflow CLI Commands

## Table of Contents

- [List DAG Runs](#list-dag-runs)
- [Clear Failed Task Instances](#clear-failed-task-instances)

---

## List DAG Runs

List runs for a specific DAG within a date range and filter for failures:

```bash
airflow dags list-runs \
  --no-backfill \
  --dag-id <DAG_ID> \
  --start-date <START_DATE> \
  --end-date <END_DATE> \
  | grep fail
```

**Example:**

```bash
airflow dags list-runs \
  --no-backfill \
  --dag-id fact_mms_transaction \
  --start-date 2025-04-10 \
  --end-date 2025-04-16 \
  | grep fail
```

---

## Clear Failed Task Instances

Re-queue only the failed task instances for a DAG within a date range:

```bash
airflow tasks clear <DAG_ID> \
  --start-date <START_DATE> \
  --end-date <END_DATE> \
  --only-failed
```

**Example:**

```bash
airflow tasks clear fact_mms_transaction \
  --start-date 2025-04-10 \
  --end-date 2025-04-16 \
  --only-failed
```
