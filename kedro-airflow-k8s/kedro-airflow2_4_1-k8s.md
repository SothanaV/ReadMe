# Kedro + Airflow 2.4.1 on Kubernetes

Deploy a Kedro pipeline as an Airflow DAG running on Kubernetes using the `KubernetesExecutor`.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Add the Airflow Helm Repository](#add-the-airflow-helm-repository)
- [Search Available Versions](#search-available-versions)
- [Create Helm Values File](#create-helm-values-file)
- [Install with Helm](#install-with-helm)
- [Upgrade](#upgrade)
- [Uninstall](#uninstall)
- [Edit the Airflow ConfigMap](#edit-the-airflow-configmap)

## Prerequisites

- A running Kubernetes cluster with `kubectl` configured
- Helm 3 installed ([helm-install.md](../kubernetes/helm-install.md))
- A container image of your Kedro project published to a registry

## Add the Airflow Helm Repository

```bash
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

helm repo add apache-airflow https://airflow.apache.org
helm repo update
```

## Search Available Versions

```bash
helm search repo apache-airflow/airflow --versions
```

## Create Helm Values File

Create `values.yml`. Replace the `repository` fields with your actual image registry paths.

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

## Install with Helm

```bash
helm install airflow apache-airflow/airflow \
  --namespace airflow \
  --create-namespace \
  --version 1.7.0 \
  -f values.yml
```

## Upgrade

```bash
helm upgrade airflow apache-airflow/airflow \
  --namespace airflow \
  --version 1.7.0 \
  -f values.yml
```

## Uninstall

```bash
helm uninstall airflow -n airflow

# Also delete persistent volume claims
kubectl delete pvc --all -n airflow
```

## Edit the Airflow ConfigMap

After installation, patch the Airflow ConfigMap to set the worker image. Locate the `[kubernetes]` section:

```ini
[kubernetes]
worker_container_repository = registry.gitlab.com/<your-group>/<your-project>
worker_container_tag = latest
image_pull_secrets = gitlab
image_pull_policy = Always
```
