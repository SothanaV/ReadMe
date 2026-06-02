# Kedro + Airflow 2.10.x on Kubernetes

Deploy a Kedro pipeline as an Airflow DAG running on Kubernetes using the `KubernetesExecutor` and `ExternalPythonOperator` with a dedicated virtual environment.

## Table of Contents

- [Part 1: Prepare the Kedro Airflow Project](#part-1-prepare-the-kedro-airflow-project)
  - [1. Create requirements-airflow.txt](#1-create-requirements-airflowtxt)
  - [2. Create the Dockerfile](#2-create-the-dockerfile)
  - [3. Create the DAG Jinja Template](#3-create-the-dag-jinja-template)
  - [4. Generate the DAG](#4-generate-the-dag)
  - [5. Build the Docker Image](#5-build-the-docker-image)
- [Part 2: Deploy on Kubernetes with Helm](#part-2-deploy-on-kubernetes-with-helm)
  - [0. Create the GitLab Registry Secret](#0-create-the-gitlab-registry-secret)
  - [1. Add the Airflow Helm Repository](#1-add-the-airflow-helm-repository)
  - [2. Check Available Versions](#2-check-available-versions)
  - [3. Create Helm Values File](#3-create-helm-values-file)
  - [4. Install or Upgrade](#4-install-or-upgrade)
  - [5. Edit the Airflow ConfigMap](#5-edit-the-airflow-configmap)
- [Troubleshooting](#troubleshooting)

---

## Part 1: Prepare the Kedro Airflow Project

### 1. Create requirements-airflow.txt

```text
asyncpg
apache-airflow-providers-fab
psycopg2-binary
pendulum
apache-airflow-providers-cncf-kubernetes
```

### 2. Create the Dockerfile

The image bundles Airflow, the pipeline code, and a separate virtual environment used by `ExternalPythonOperator` to run Kedro nodes in isolation.

```dockerfile
FROM apache/airflow:slim-2.10.5-python3.12

USER root
RUN apt-get update --fix-missing && \
    apt-get install -y git netcat-traditional curl iputils-ping libpq-dev gcc unzip wget libaio1 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/airflow

USER airflow
COPY ./etl-pipeline/requirements-airflow.txt /requirements-airflow.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements-airflow.txt

COPY ./etl-pipeline/requirements.txt /requirements.txt
RUN pip install virtualenv
RUN python -m venv /home/airflow/venv && \
    source /home/airflow/venv/bin/activate && \
    pip install -r /requirements.txt && \
    ls /home/airflow/venv/bin/activate

COPY ./etl-pipeline /opt/airflow/dags

USER root
RUN chmod -R 777 /opt/airflow/dags

USER airflow
```

### 3. Create the DAG Jinja Template

Save the following as `dags-template.j2` alongside `pyproject.toml`. This template is rendered by `kedro airflow create` to produce a DAG file.

```python
from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python import ExternalPythonOperator


def kedro_run(
    package_name: str,
    pipeline_name: str,
    node_name: str | list[str],
    project_path: str,
    env: str,
    conf_source: str,
    **kwargs
):
    from kedro.framework.session import KedroSession
    from kedro.framework.project import configure_project
    from kedro.framework.startup import bootstrap_project

    print(f"kwargs : {kwargs}")

    print("bootstrap_project")
    bootstrap_project(project_path)
    print("bootstrap_project done")

    configure_project(package_name)
    session = KedroSession.create(
        project_path,
        env=env,
        conf_source=conf_source,
        extra_params={
            'etl_date': kwargs['ds']
        }
    )
    if isinstance(node_name, str):
        node_name = [node_name]
    session.run(pipeline_name, node_names=node_name)


venv_cache_path = "/home/airflow/venv/"
project_path = "/opt/airflow/dags"
env = "local"
conf_source = "/opt/airflow/dags/conf"
package_name = "{{ package_name }}"
pipeline_name = "{{ pipeline_name }}"


with DAG(
    dag_id="{{ dag_name | safe | slugify }}",
    start_date=datetime({{ start_date | default([2023, 1, 1]) | join(",")}}),
    max_active_runs={{ max_active_runs | default(3) }},
    # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
    schedule_interval="{{ schedule_interval | default('@once') }}",
    catchup={{ catchup | default(False) }},
    default_args=dict(
        owner="{{ owner | default('airflow') }}",
        depends_on_past={{ depends_on_past | default(False) }},
        email_on_failure={{ email_on_failure | default(False) }},
        email_on_retry={{ email_on_retry | default(False) }},
        retries={{ retries | default(1) }},
        retry_delay=timedelta(minutes={{ retry_delay | default(5) }})
    )
) as dag:
    tasks = {
    {% for group, data in node_objs.items() %}
        "{{ data.name | slugify }}": ExternalPythonOperator(
            task_id="{{ data.name | slugify }}",
            python_callable=kedro_run,
            python="/home/airflow/venv/bin/python",
            op_kwargs={
                "package_name": package_name,
                "pipeline_name": pipeline_name,
                "node_name": {% if data.nodes | length > 1 %}[{% endif %}{% for node in data.nodes %}"{{ node.name }}"{% if not loop.last %}, {% endif %}{% endfor %}{% if data.nodes | length > 1 %}]{% endif %},
                "project_path": project_path,
                "env": env,
                "conf_source": conf_source,
            }
        ){% if not loop.last %},{% endif %}
    {% endfor %}
    }

    {% for group, data in node_objs.items() %}
    {% for dep in data.dependencies %}
    tasks["{{ dep | slugify }}"] >> tasks["{{ data.name | slugify }}"]
    {% endfor %}
    {% endfor %}
```

### 4. Generate the DAG

```bash
kedro airflow create \
  --target-dir ./airflow_dags/ \
  --jinja-file ./dags-template.j2 \
  --pipeline <PIPELINE_NAME>
```

### 5. Build the Docker Image

Build and push using your preferred method (manual `docker build` or CI/CD pipeline).

---

## Part 2: Deploy on Kubernetes with Helm

### 0. Create the GitLab Registry Secret

Create `gitlab.yml` with your base64-encoded Docker config JSON:

```yaml
apiVersion: v1
kind: Secret
type: kubernetes.io/dockerconfigjson
metadata:
  name: gitlab
  namespace: kedro
data:
  .dockerconfigjson: >-
    ewogICJhdXRocyI6IHsKICAgICJyZWdpc3RyeS5naXRsYWIuY29tIjogewogICAgICAidXNlcm5hbWUiOiAiZGVwbG95IiwKICAgICAgInBh....
```

```bash
kubectl apply -f gitlab.yml
```

### 1. Add the Airflow Helm Repository

```bash
helm repo add apache-airflow https://airflow.apache.org
helm repo update
```

### 2. Check Available Versions

```bash
helm search repo apache-airflow/airflow --versions
```

Example output:

```text
NAME                    CHART VERSION   APP VERSION     DESCRIPTION
apache-airflow/airflow  1.18.0          3.0.2           The official Helm chart to deploy Apache Airflow
apache-airflow/airflow  1.17.0          3.0.2           The official Helm chart to deploy Apache Airflow
apache-airflow/airflow  1.16.0          2.10.5          The official Helm chart to deploy Apache Airflow
apache-airflow/airflow  1.15.0          2.9.3           The official Helm chart to deploy Apache Airflow
```

> The `APP VERSION` in the chart must match the base image version used in your Dockerfile.

### 3. Create Helm Values File

Create `airflow-values.yml`:

```yaml
executor: KubernetesExecutor

registry:
  secretName: gitlab

logs:
  persistence:
    enabled: true
    size: 10Gi

securityContext:
  runAsUser: 50000
  fsGroup: 1001

images:
  airflow:
    repository: registry.gitlab.com/<your-group>/<your-project>
    tag: latest
    pullPolicy: Always
  useDefaultImageForMigration: true
  pod_template:
    repository: registry.gitlab.com/<your-group>/<your-project>
    tag: latest
    pullPolicy: Always
```

### 4. Install or Upgrade

**First install:**

```bash
helm install airflow apache-airflow/airflow \
  --namespace airflow \
  --create-namespace \
  --version 1.16.0 \
  -f airflow-values.yml
```

**Upgrade:**

```bash
helm upgrade airflow apache-airflow/airflow \
  --namespace airflow \
  --version 1.16.0 \
  -f airflow-values.yml
```

**Uninstall:**

```bash
helm uninstall airflow -n airflow

# Also delete persistent volume claims
kubectl delete pvc --all -n airflow
```

### 5. Edit the Airflow ConfigMap

Locate the `[kubernetes]` section in the Airflow ConfigMap and update the worker image settings:

```ini
[kubernetes]
worker_container_repository = registry.gitlab.com/<your-group>/<your-project>
worker_container_tag = latest
image_pull_secrets = gitlab
image_pull_policy = Always
```

---

## Troubleshooting

### Permission errors on the logs directory

If the webserver or scheduler fails due to log directory ownership, add an `initContainer` to the affected deployment to fix permissions at startup:

```yaml
initContainers:
  - name: fix-log-permissions
    image: busybox
    command: ["sh", "-c", "chown -R 50000:1001 /opt/airflow/logs"]
    volumeMounts:
      - name: logs
        mountPath: /opt/airflow/logs
    securityContext:
      runAsUser: 0  # run as root to change ownership
```
