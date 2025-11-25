# How to Kubenetes Ingress use service in other namespace
1. create new service `service.yml`
```yml
apiVersion: v1
kind: Service
metadata:
  name: clickhouse # servicename
  namespace: dataplatform # namespace to ingress
spec:
  ports:
    - protocol: TCP
      port: 8123
      targetPort: 8123
  type: ExternalName
  sessionAffinity: None
  externalName: clickhouse.vquery.svc.cluster.local # endpoint to use service on othernamespace
```
- apply it's
```
kubectl apply -f service.yml
```

2. edit/create ingress `ingress.yml`
```yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: query-service
  namespace: dataplatform
  ingressClassName: nginx
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

- apply it's
```
kubectl apply -f ingress.yml
```