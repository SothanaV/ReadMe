# K8S Tips

## select running node
```
spec:
	template:
		spec:
			container:
			...
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