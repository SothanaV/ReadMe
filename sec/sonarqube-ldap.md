# SonarQube LDAP Configuration

This guide explains how to configure SonarQube to authenticate users via LDAP in a Kubernetes environment.

## Step 1: Create or Update the ConfigMap

Create a file named `sonarqube-sonarqube-config.yaml` with the following content:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: sonarqube-sonarqube-config
  namespace: sonarqube
spec: {}
data:
  sonar.properties: >-
    sonar.security.realm=LDAP
    ldap.url=ldap://<host>:<port>
    ldap.bindDn=xxxxx
    ldap.bindPassword=****
    ldap.user.baseDn=dc=xxx,dc=yyy,dc=com
    ldap.user.request=(&(objectClass=user)(sAMAccountName={login}))
    ldap.user.realNameAttribute=cn
    ldap.user.emailAttribute=mail
```

Apply the ConfigMap:

```bash
kubectl apply -f sonarqube-sonarqube-config.yaml
```

## Step 2: Update the StatefulSet or Deployment

Modify your SonarQube StatefulSet or Deployment to mount the ConfigMap as a `sonar.properties` file:

```yaml
spec:
  template:
    spec:
      volumes:
        - name: config
          configMap:
            name: sonarqube-sonarqube-config
            defaultMode: 420
      containers:
        - name: sonarqube
          # ... existing container config ...
          volumeMounts:
            - name: config
              mountPath: /opt/sonarqube/conf/sonar.properties
              subPath: sonar.properties
```

## Step 3: Restart SonarQube

After applying the changes, restart the SonarQube pods:

```bash
kubectl rollout restart deployment/sonarqube-sonarqube -n sonarqube
# OR if using StatefulSet:
# kubectl rollout restart statefulset/sonarqube-sonarqube -n sonarqube
```

## Additional LDAP Configuration Options

### SSL/TLS Configuration

If you need to use LDAPS, update the `ldap.url` property and add SSL settings:

```properties
ldap.url=ldaps://<host>:<port>
ldap.trustStore=/path/to/truststore
ldap.trustStorePassword=your-password
```

### Group Synchronization

To sync LDAP groups with SonarQube:

```properties
ldap.group.request=(&(objectClass=group)(member={dn}))
ldap.group.baseDn=dc=xxx,dc=yyy,dc=com
ldap.group.idAttribute=cn
```

### Active Directory Example

For Active Directory environments, a more complete configuration:

```properties
sonar.security.realm=LDAP
ldap.url=ldap://ad.example.com:389
ldap.bindDn=CN=svc-sonar,OU=ServiceAccounts,DC=example,DC=com
ldap.bindPassword=your-password
ldap.user.baseDn=DC=example,DC=com
ldap.user.request=(&(objectClass=user)(sAMAccountName={login}))
ldap.user.realNameAttribute=cn
ldap.user.emailAttribute=mail
ldap.group.request=(&(objectClass=group)(member={dn}))
ldap.group.baseDn=DC=example,DC=com
ldap.group.idAttribute=cn