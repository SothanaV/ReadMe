# NGINX Redirect Kubernetes Deployment

This project provides a Kubernetes-based NGINX configuration to redirect incoming HTTP traffic from one domain/path to another. Replace `YOUR_DOMAIN` in the configuration with your actual domain before deploying.

## Overview

The setup uses NGINX running in a Kubernetes cluster to perform permanent (301) redirects. This is useful for:

- Migrating services to new paths or domains
- Creating alias endpoints for existing services (e.g., Grafana)
- Load balancer or ingress abstraction

## Architecture

```
Client Request
     ↓
YOUR_DOMAIN:3000
     ↓
NGINX Redirect (301)
     ↓
https://YOUR_DOMAIN/grafana/<original-path>
```

## Kubernetes Resources

### 1. ConfigMap (`nginx-redirect-config`)

Stores the NGINX server configuration in `/etc/nginx/conf.d/default.conf`.

**Configuration Details:**
- Listens on port `3000`
- Server name: `_` (catches all hostnames)
- Returns a `301 Permanent Redirect` to `https://YOUR_DOMAIN/grafana$request_uri`
- `$request_uri` preserves the original path and query string
- **Important:** Replace `YOUR_DOMAIN` with your actual domain before deploying

### 2. Deployment (`nginx-redirect`)

Runs the NGINX container with the following specifications:

| Property       | Value            |
|---------------|------------------|
| Replicas      | 1                |
| Image         | `nginx:alpine`   |
| Container Port| `3000`           |
| ConfigMap Mount| `/etc/nginx/conf.d/default.conf` (subPath) |

### 3. Service (`nginx-redirect-service`)

Exposes the NGINX deployment on port `3000`.

| Property      | Value           |
|--------------|-----------------|
| Type         | `LoadBalancer`  |
| Port         | `3000`          |
| Target Port  | `3000`          |

> **Note:** Change the service type based on your environment:
> - **Cloud providers (AWS/GCP/Azure):** Use `LoadBalancer`
> - **On-premise / Minikube:** Use `NodePort` or `ClusterIP` with an Ingress controller

## Files

```
redirect/
├── nginx-redirect.yaml   # Kubernetes manifests (ConfigMap, Deployment, Service)
└── README.md             # This file
```

## Deployment

### Apply the Configuration

```bash
kubectl apply -f nginx-redirect.yaml
```

### Verify Deployment

```bash
# Check pods
kubectl get pods -l app=nginx-redirect

# Check service
kubectl get svc nginx-redirect-service

# Check ConfigMap
kubectl get configmap nginx-redirect-config -o yaml
```

### Test the Redirect

```bash
# Request any path on the redirect endpoint
curl -I http://YOUR_DOMAIN:3000/some/path

# Expected response header:
# HTTP/1.1 301 Moved Permanently
# Location: https://YOUR_DOMAIN/grafana/some/path
```

## Customization

### Change Redirect Target

Edit the `return` directive in `nginx-redirect.yaml`:

```nginx
return 301 https://YOUR_DOMAIN/grafana$request_uri;
```

### Change HTTP Status Code

- `301` — Permanent redirect (cached by browsers)
- `302` — Temporary redirect (not cached)

```nginx
return 302 https://YOUR_DOMAIN/grafana$request_uri;
```

### Change Listening Port

Update both the `listen` directive and the `containerPort` / `port` / `targetPort` values:

```nginx
listen 8080;
```

```yaml
ports:
  - containerPort: 8080
    port: 8080
    targetPort: 8080
```

### Increase Replicas

```yaml
replicas: 3
```

## Troubleshooting

### NGINX not reloading config

If changes to the ConfigMap don't take effect, restart the pod:

```bash
kubectl rollout restart deployment nginx-redirect
```

### Service not accessible

- Verify the service type matches your cluster setup
- Check if a firewall or security group allows traffic on port `3000`
- For cloud providers, ensure the LoadBalancer external IP is assigned

### SSL/TLS Issues

The redirect targets `https://`. Ensure the target domain has a valid SSL certificate. If using a self-signed certificate, add `ssl_verify_client off;` or configure proper CA trust.

## License

This project is provided as-is for configuration reference purposes.