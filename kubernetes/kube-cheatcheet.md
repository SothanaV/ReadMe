# Kubectl Cheat Sheet

- get name and IP
```sh
kubectl get nodes -o custom-columns="NAME:.metadata.name,IP_ADDRESS:.status.addresses[0].address"
```

- delete pod by status
    - phase
        - Pending
        - Running
        - Succeeded
        - Failed
```sh
kubectl delete pods --field-selector status.phase=Failed
```