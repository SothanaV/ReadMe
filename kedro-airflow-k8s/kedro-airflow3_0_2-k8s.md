# Kedro + Airflow 3.0.x on Kubernetes

Deploy a Kedro pipeline as an Airflow DAG running on Kubernetes using the `KubernetesExecutor` and `ExternalPythonOperator` with a dedicated virtual environment.

## Table of Contents

- [Part 1: Prepare the Kedro Airflow Project](#part-1-prepare-the-kedro-airflow-project)
  - [1. Create requirements-airflow.txt](#1-create-requirements-airflowtxt)
  - [2. Create the Dockerfile](#2-create-the-dockerfile)
  - [3. Create the DAG Jinja Template](#3-create-the-dag-jinja-template)
  - [4. Install kedro-airflow](#4-install-kedro-airflow)
  - [5. Generate the DAG](#5-generate-the-dag)
  - [6. Build the Docker Image](#6-build-the-docker-image)
- [Part 2: Deploy on Kubernetes with Helm](#part-2-deploy-on-kubernetes-with-helm)
  - [0. Create the GitLab Registry Secret](#0-create-the-gitlab-registry-secret)
  - [1. Add the Airflow Helm Repository](#1-add-the-airflow-helm-repository)
  - [2. Check Available Versions](#2-check-available-versions)
  - [3. Create Helm Values File](#3-create-helm-values-file)
  - [4. Install or Upgrade](#4-install-or-upgrade)
  - [5. Edit the Airflow ConfigMap](#5-edit-the-airflow-configmap)
- [Email Alerts on Task Failure](#email-alerts-on-task-failure)
- [Troubleshooting](#troubleshooting)
- [Run Airflow Behind a Proxy](#run-airflow-behind-a-proxy)

---

## Part 1: Prepare the Kedro Airflow Project

### 1. Create requirements-airflow.txt

```text
asyncpg==0.30.0
apache-airflow-providers-fab==2.3.0
apache-airflow-providers-cncf-kubernetes==10.6.1
psycopg2-binary==2.9.10
pendulum==3.1.0
statsd==4.0.1
triad==0.9.8
```

Also update `requirements.txt` with any version pins needed for compatibility:

```text
pendulum==3.1.0
lazy_object_proxy==1.11.0
```

### 2. Create the Dockerfile

The image bundles Airflow 3.0.2, the pipeline code, and a separate virtual environment used by `ExternalPythonOperator` to run Kedro nodes in isolation.

```dockerfile
FROM apache/airflow:slim-3.0.2-python3.12

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


venv_cache_path = "/home/airflow/venv"
venv_python_path = f"{venv_cache_path}/bin/python"
project_path = "/opt/airflow/dags"
env = "local"
conf_source = "/opt/airflow/dags/conf"
package_name = "{{ package_name }}"
pipeline_name = "{{ pipeline_name }}"


with DAG(
    dag_id="{{ pipeline_name | safe | slugify }}",
    start_date=datetime({{ start_date | default([2023, 1, 1]) | join(",")}}),
    max_active_runs={{ max_active_runs | default(3) }},
    # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
    schedule="{{ schedule_interval | default('@once') }}",
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
            python=venv_python_path,
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

### 4. Install kedro-airflow

```bash
pip install kedro-airflow
```

### 5. Generate the DAG

```bash
kedro airflow create \
  --target-dir ./airflow_dags/ \
  --jinja-file ./dags-template.j2 \
  --pipeline <PIPELINE_NAME>
```

### 6. Build the Docker Image

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

Create `airflow-values.yml`. The `dagProcessor.extraInitContainers` block pre-fixes log directory ownership on startup.

```yaml
airflowVersion: "3.0.6"
defaultAirflowTag: "3.0.6"
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

postgresql:
  image:
    repository: bitnamilegacy/postgresql

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

dagProcessor:
  extraInitContainers:
    - name: fix-log-permissions
      image: busybox
      command:
        - sh
        - -c
        - chown -R 50000:1001 /opt/airflow/logs
      volumeMounts:
        - name: logs
          mountPath: /opt/airflow/logs
      securityContext:
        runAsUser: 0

apiServer:
  apiServerConfig: |
    from __future__ import annotations

    import os
    import requests
    from flask_appbuilder.security.manager import AUTH_OAUTH, AUTH_DB
    from airflow.providers.fab.auth_manager.security_manager.override import FabAirflowSecurityManagerOverride

    basedir = os.path.abspath(os.path.dirname(__file__))

    WTF_CSRF_ENABLED = True

    # AUTH_TYPE = AUTH_OAUTH
    AUTH_TYPE = AUTH_DB
    OAUTH_PROVIDERS = [{
        'name': 'dsm',
        'token_key': 'access_token',
        'icon': 'fa-lock',
        'remote_app': {
            'api_base_url': 'http://oauth.dataplatform:18000/api/v1/account/me/',
            'access_token_url': 'http://oauth.dataplatform:18000/o/token/',
            'authorize_url': 'https://oauth-dev-ins.example.com/o/authorize',
            'request_token_url': None,
            'client_id': '',
            'client_secret': '',
        }
    }]


    class CustomSecurity(FabAirflowSecurityManagerOverride):

        def sync_roles(self):
            pass  # Skip default role sync

        def get_oauth_user_info(self, provider, response=None):
            if provider == 'dsm':
                config = {}
                for elm in OAUTH_PROVIDERS:
                    if elm.get('name') == 'dsm':
                        config = elm.get('remote_app')
                res = requests.get(config.get('api_base_url'), headers={
                    'Authorization': f"{response.get('token_type')} {response.get('access_token')}"
                })
                if res.status_code != 200:
                    print(res.text)
                    return {}
                me = res.json()
                print(me)
                return {
                    'email': me['email'],
                    'first_name': me['first_name'],
                    'last_name': me['last_name'],
                    'username': me['username'],
                    'role_keys': ['Admin', 'Viewer'],
                }
            return {}

    # SECURITY_MANAGER_CLASS = CustomSecurity
    AUTH_USER_REGISTRATION = True
    AUTH_ROLES_SYNC_AT_LOGIN = True
    AUTH_USER_REGISTRATION_ROLE = 'Admin'
```

### 4. Install or Upgrade

**First install:**

```bash
helm install airflow apache-airflow/airflow \
  --namespace airflow \
  --create-namespace \
  --version 1.18.0 \
  -f airflow-values.yml
```

**Upgrade:**

```bash
helm upgrade airflow apache-airflow/airflow \
  --namespace airflow \
  --version 1.18.0 \
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

## Email Alerts on Task Failure

### Update dags-template.j2

Add the failure callback and email utility imports to `dags-template.j2`:

```python
from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python import ExternalPythonOperator
from airflow.models import Variable

from dsm_services.airflow import utils as email_utils
import dsmemail

DSM_EMAIL_URI    = Variable.get("DSM_EMAIL_URI",    default_var="https://email-service.data.storemesh.com", deserialize_json=False)
DSM_EMAIL_APIKEY = Variable.get("DSM_EMAIL_APIKEY", default_var="API_KEY",                                  deserialize_json=False)
SITE_NAME        = Variable.get("SITE_NAME",        default_var='',                                         deserialize_json=False)
ALERT_EMAILS     = Variable.get("ALERT_EMAILS",     default_var='[]',                                       deserialize_json=True)


def task_failure_alert(context):
    print(context)
    print(ALERT_EMAILS)
    subject, body = email_utils.create_notice_email(site_name=SITE_NAME, context=context)
    status = dsmemail.sendEmail(
        subject=subject,
        message=body,
        emails=ALERT_EMAILS,
        host=DSM_EMAIL_URI,
        api_key=DSM_EMAIL_APIKEY
    )
    print(status)


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
    bootstrap_project(project_path)
    configure_project(package_name)
    session = KedroSession.create(
        project_path,
        env=env,
        conf_source=conf_source,
        extra_params={'etl_date': kwargs['ds']}
    )
    if isinstance(node_name, str):
        node_name = [node_name]
    session.run(pipeline_name, node_names=node_name)


venv_cache_path = "/home/airflow/venv/"
project_path    = "/opt/airflow/dags"
env             = "local"
conf_source     = "/opt/airflow/dags/conf"
package_name    = "{{ package_name }}"
pipeline_name   = "{{ pipeline_name }}"


with DAG(
    dag_id="{{ pipeline_name | safe | slugify }}",
    start_date=datetime({{ start_date | default([2023, 1, 1]) | join(",")}}),
    max_active_runs={{ max_active_runs | default(3) }},
    schedule="{{ schedule_interval | default('@once') }}",
    catchup={{ catchup | default(False) }},
    default_args=dict(
        owner="{{ owner | default('airflow') }}",
        depends_on_past={{ depends_on_past | default(False) }},
        email_on_failure={{ email_on_failure | default(False) }},
        email_on_retry={{ email_on_retry | default(False) }},
        retries={{ retries | default(1) }},
        retry_delay=timedelta(minutes={{ retry_delay | default(5) }}),
        on_failure_callback=task_failure_alert
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

### Add email packages to requirements-airflow.txt

```text
dsmemail==0.0.7
dsm-services==0.0.13
```

### Configure Airflow Variables

Add the following variables in the Airflow UI under **Admin > Variables**:

| Variable | Type | Description |
| --- | --- | --- |
| `SITE_NAME` | String | Site name used in the email subject line |
| `DSM_EMAIL_URI` | String | Email service base URL (e.g. `https://email-service.data.storemesh.com`) |
| `DSM_EMAIL_APIKEY` | String | API key for the DSM email service |
| `ALERT_EMAILS` | JSON (array) | List of recipient addresses, e.g. `["user@example.com"]` |

---

## Troubleshooting

### Permission errors on the logs directory

If the webserver or scheduler fails due to log directory ownership, add an `initContainer` to the affected deployment:

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

### NoneType error on FAB permissions

If you see the following traceback:

```log
File ".../airflow/providers/fab/auth_manager/models/__init__.py", line 287, in perms
    (perm.action.name, perm.resource.name) for role in self.roles for perm in role.permissions
AttributeError: 'NoneType' object has no attribute 'name'
```

This is caused by orphaned rows in the `ab_permission_view` table. Connect to the Airflow metadata database and clean them up:

```python
import pandas as pd
import os
import sqlalchemy

con = os.environ.get('AIRFLOW_CONN_AIRFLOW_DB')
eng = sqlalchemy.create_engine(con)
conn = eng.raw_connection()

# Inspect orphaned rows
pd.read_sql_query("""
SELECT * FROM ab_permission_view
WHERE permission_id IS NULL
""", conn)

# Remove orphaned rows
cur = conn.cursor()
cur.execute("""
DELETE FROM ab_permission_view
WHERE permission_id IS NULL
""")
conn.commit()
```

## Run Airflow Behind a Proxy

Example using subpath `airflow-temp`.

### 1. Add environment variables to the API server deployment

```yaml
containers:
  env:
    - name: AIRFLOW__API__BASE_URL
      value: https://your-domain.com/airflow-temp/
    - name: FORWARDED_ALLOW_IPS
      value: "*"
```

### 2. Update `airflow.cfg`

```ini
[core]
execution_api_server_url = http://airflow-api-server:8080/airflow-temp/execution/

[webserver]
enable_proxy_fix = True
base_url = https://your-domain.com/airflow-temp/
```

### 3. Create Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: airflow-api
  namespace: airflow-temp
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - your-domain.com
      secretName: your-tls-secret
  rules:
    - host: your-domain.com
      http:
        paths:
          - path: /airflow-temp/
            pathType: Prefix
            backend:
              service:
                name: airflow-api-server
                port:
                  number: 8080
```