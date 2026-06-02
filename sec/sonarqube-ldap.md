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
data:
  sonar.properties: |
    sonar.security.realm=LDAP
    ldap.url=ldap://<host>:<port>
    ldap.bindDn=<bind-dn>
    ldap.bindPassword=<bind-password>
    ldap.user.baseDn=dc=example,dc=com
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
# If using a Deployment
kubectl rollout restart deployment/sonarqube-sonarqube -n sonarqube

# If using a StatefulSet
kubectl rollout restart statefulset/sonarqube-sonarqube -n sonarqube
```

## Additional LDAP Configuration Options

### SSL/TLS Configuration

To use LDAPS (LDAP over TLS), update the `ldap.url` property and add the trust store settings:

```properties
ldap.url=ldaps://<host>:<port>
ldap.trustStore=/path/to/truststore.jks
ldap.trustStorePassword=<truststore-password>
```

### Group Synchronization

To sync LDAP groups with SonarQube roles:

```properties
ldap.group.baseDn=dc=example,dc=com
ldap.group.request=(&(objectClass=group)(member={dn}))
ldap.group.idAttribute=cn
```

### Active Directory Example

A complete configuration for an Active Directory environment:

```properties
sonar.security.realm=LDAP
ldap.url=ldap://ad.example.com:389
ldap.bindDn=CN=svc-sonar,OU=ServiceAccounts,DC=example,DC=com
ldap.bindPassword=<service-account-password>
ldap.user.baseDn=DC=example,DC=com
ldap.user.request=(&(objectClass=user)(sAMAccountName={login}))
ldap.user.realNameAttribute=cn
ldap.user.emailAttribute=mail
ldap.group.baseDn=DC=example,DC=com
ldap.group.request=(&(objectClass=group)(member={dn}))
ldap.group.idAttribute=cn
```
