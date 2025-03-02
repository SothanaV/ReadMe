# Install airflow kedro
```
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
helm repo add apache-airflow https://airflow.apache.org
helm repo update
```

```
helm search repo apache-airflow/airflow --versions
```

- create values.yml
```
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
```

- first install
```
helm install airflow apache-airflow/airflow --namespace airflow --create-namespace --version 1.7.0 -f values.yml
```

- update
```
helm upgrade airflow apache-airflow/airflow --namespace airflow --version 1.7.0 -f values.yml
```

- uninstall
```
helm uninstall airflow -n airflow
# delete pv
kubectl delete pvc --all -n airflow
```

- edit configmap
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