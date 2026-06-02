# Kubernetes Ingress: Routing to a Service in Another Namespace

Kubernetes Ingress rules are namespace-scoped, so they cannot directly reference a Service in a different namespace. The solution is to create an `ExternalName` Service in the Ingress namespace that acts as a proxy to the target Service in the other namespace.

## Table of Contents

- [Overview](#overview)
- [Step 1: Create an ExternalName Service](#step-1-create-an-externalname-service)
- [Step 2: Create or Update the Ingress](#step-2-create-or-update-the-ingress)

## Overview

The approach uses a Kubernetes `ExternalName` Service as a bridge between namespaces. The Ingress in namespace `dataplatform` references a local Service that resolves to the fully qualified cluster DNS name of the upstream Service in namespace `vquery`.

## Step 1: Create an ExternalName Service

Create `service.yml` in the Ingress namespace. The `externalName` field must be the fully qualified in-cluster DNS name of the target Service.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: clickhouse
  namespace: dataplatform   # namespace where the Ingress lives
spec:
  type: ExternalName
  externalName: clickhouse.vquery.svc.cluster.local  # target service in another namespace
  sessionAffinity: None
  ports:
    - protocol: TCP
      port: 8123
      targetPort: 8123
```

Apply the Service:

```bash
kubectl apply -f service.yml
```

## Step 2: Create or Update the Ingress

Create `ingress.yml`. The Ingress routes `/clickhouse` traffic to the `ExternalName` Service created above.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: query-service
  namespace: dataplatform
  annotations:
    ingressClassName: nginx
spec:
  tls:
    - hosts:
        - api-service.xx.yy.com
      secretName: ingress-cert
  rules:
    - host: api-service.xx.yy.com
      http:
        paths:
          - path: /api
            pathType: ImplementationSpecific
            backend:
              service:
                name: nginx-query-service
                port:
                  number: 8973
          - path: /clickhouse
            pathType: Prefix
            backend:
              service:
                name: clickhouse
                port:
                  number: 8123
```

Apply the Ingress:

```bash
kubectl apply -f ingress.yml
```
