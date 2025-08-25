# Kedro Airflow k8s
## Prepair kedro airflow
1. create `requirements-airflow.txt`
```
asyncpg==0.30.0
apache-airflow-providers-fab==2.3.0
apache-airflow-providers-cncf-kubernetes==10.6.1
psycopg2-binary==2.9.10
pendulum==3.1.0
statsd==4.0.1
triad==0.9.8
```

update `requirements.txt`
```
...
pendulum==3.1.0
lazy_object_proxy==1.11.0
...
```

2. create `Dockerfile`
```Dockerfile
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
    source /home/airflow/venv/bin/activate &&\
    pip install -r /requirements.txt && \
    ls /home/airflow/venv/bin/activate

COPY ./etl-pipeline /opt/airflow/dags

USER root
RUN chmod -R 777 /opt/airflow/dags

USER airflow
```

3. copy `dags-template.j2` along side `project.toml`
```sh
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
    dag_id="{{ pipeline_name | safe | slugify }}",
    start_date=datetime({{ start_date | default([2023, 1, 1]) | join(",")}}),
    max_active_runs={{ max_active_runs | default(3) }},
    # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
    schedule="{{ schedule_interval | default('@once') }}",
    catchup={{ catchup | default(False) }},
    # Default settings applied to all tasks
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

4. install kedro airflow
```
pip install kedro-airflow
```
5. create DAG
```
kedro airflow create --target-dir ./airflow_dags/ --jinja-file ./dags-template.j2 --pipeline <PIPELINE_NAME>
```

6. build docker image
  - manual build
  - ci/cd


## deploy on k8s using helm
0. create gitlab secret `gitlab.yml`
```yml
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
```
kubectl apply -f gitlab.yml
```
1. add airflow repo
```
helm repo add apache-airflow https://airflow.apache.org
helm repo update
```

2. search chech helm and airflow version
```
helm search repo apache-airflow/airflow --versions
```
```
NAME                    CHART VERSION   APP VERSION     DESCRIPTION                                       
apache-airflow/airflow  1.18.0          3.0.2           The official Helm chart to deploy Apache Airflo...
apache-airflow/airflow  1.17.0          3.0.2           The official Helm chart to deploy Apache Airflo...
apache-airflow/airflow  1.16.0          2.10.5          The official Helm chart to deploy Apache Airflo...
apache-airflow/airflow  1.15.0          2.9.3           The official Helm chart to deploy Apache Airflo...
```

APP VERSION must be align docker image 

3. create airflow-values.yml
```yml
executor: KubernetesExecutor
registry:
  secretName: gitlab
logs:
  persistence:
    enabled: true
    size: 10Gi  # Adjust based on your needs
securityContext:
  runAsUser: 50000
  fsGroup: 1001

images:
  airflow:
    repository: registry.gitlab.com/...
    tag: latest
    pullPolicy: Always
  useDefaultImageForMigration: true
  pod_template:
    repository: registry.gitlab.com/...
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
```

4. install

 - first install
    ```
    helm install airflow apache-airflow/airflow --namespace airflow --create-namespace --version 1.18.0 -f airflow-values.yml
    ```

 - update
    ```
    helm upgrade airflow apache-airflow/airflow --namespace airflow --version 1.18.0 -f values.yml
    ```

    - uninstall
    ```
    helm uninstall airflow -n airflow
    # delete pv
    kubectl delete pvc --all -n airflow
    ```

5. edit configmap

    - airflow config
    ```
    [kubernetes]
    ...
    worker_container_repository = registry.gitlab.com/...
    worker_container_tag = latest
    image_pull_secrets = gitlab
    image_pull_policy = Always
    ...
    ```

![airflow-ui](/_asset/airflowv3-ui.png)

![airflow-k3s](/_asset/airflowv3-k3s.png)

### If have permission problem
add webserver and scheduler deployment
```yml
initContainers:
  - name: fix-log-permissions
    image: busybox
    command: ["sh", "-c", "chown -R 50000:1001 /opt/airflow/logs"]
    volumeMounts:
      - name: logs
        mountPath: /opt/airflow/logs
    securityContext:
      runAsUser: 0 # run as root to change ownership
```