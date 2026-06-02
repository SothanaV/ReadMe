# Kubernetes Tips

## Table of Contents

- [Pin Pods to Specific Nodes](#pin-pods-to-specific-nodes)

## Pin Pods to Specific Nodes

Use `nodeAffinity` in the pod spec to restrict scheduling to a named set of nodes. The example below requires the pod to be placed on `node1`, `node2`, or `node3`.

```yaml
spec:
  template:
    spec:
      containers:
        # ... container definitions ...
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: kubernetes.io/hostname
                    operator: In
                    values:
                      - node1
                      - node2
                      - node3
```
