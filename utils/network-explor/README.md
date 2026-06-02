# Network Explorer

A Docker-based network diagnostic toolset that bundles common network utilities into a single container image. Useful for troubleshooting network connectivity inside Kubernetes clusters or Docker environments.

## Build the Image

```bash
docker build --platform linux/amd64 -t sothanaii/network-tools:latest .
```

## Publish to Docker Registry

```bash
docker push sothanaii/network-tools:latest
```

## Docker Usage

Run an interactive shell with all network tools available:

```bash
docker run --rm -it --entrypoint bash sothanaii/network-tools
```

## Kubernetes Usage

Deploy as a DaemonSet to run the network tools on every node in the cluster:

```bash
kubectl apply -f network-check-daemonset.yml
```

See the DaemonSet manifest for full configuration details: [network-check-daemonset.yml](./network-check-daemonset.yml)

## Common Network Commands

Once inside the container, you can use tools such as:

```bash
# Check DNS resolution
nslookup <hostname>
dig <hostname>

# Test connectivity
ping <host>
curl -v <url>

# Inspect routes
ip route
traceroute <host>

# Port scan / connectivity check
nc -zv <host> <port>
```
