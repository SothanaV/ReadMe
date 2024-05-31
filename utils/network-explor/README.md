# Network Explor

## Create image 
- build image
```
docker build --platform linux/amd64 -t sothanaii/network-tools:latest .
```

- push to docker regietry
```
docker push sothanaii/network-tools:latest
```

# Docker usage
```
docker run --rm -it --entrypoint bash sothanaii/network-tools
```

# Kubenetes usage
```
kubectl apply -f network-check-daemonset.yml
```

see more <a href="./network-check-daemonset.yml"> network-check-daemonset.yml</a>