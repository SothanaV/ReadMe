# Kubectl Cheat Sheet

## Table of Contents

- [Nodes](#nodes)
- [Pods](#pods)

## Nodes

### Get node names and IP addresses

```bash
kubectl get nodes -o custom-columns="NAME:.metadata.name,IP_ADDRESS:.status.addresses[0].address"
```

## Pods

### Delete pods by phase

Valid phase values: `Pending`, `Running`, `Succeeded`, `Failed`

```bash
kubectl delete pods --field-selector status.phase=Failed
```
