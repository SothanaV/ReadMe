# SonarQube Plugins

## From UI

### Using the Marketplace (Community Edition/Build)

If your SonarQube instance has internet access and you are using the Community Build:

1. Log in as a System Administrator.
2. Navigate to **Administration > Marketplace**.
3. Use the search bar to find the plugin you need.
4. Click **Install**.
5. Once the download completes, a prompt will appear at the top of the page. Click **Restart** to apply the changes.

---

## CLI (Manual Install)

Use this method when the SonarQube instance has no internet access or you need a specific plugin version.

### 1. Exec into the SonarQube pod/container

```bash
kubectl exec -it <sonarqube-pod> -- /bin/bash
```

### 2. Download and install the plugin

```bash
mkdir -p /opt/sonarqube/extensions/plugins
cd /opt/sonarqube/extensions/plugins

# Example: sonar-cxx plugin
curl -L -O https://github.com/SonarOpenCommunity/sonar-cxx/releases/download/cxx-2.2.2/sonar-cxx-plugin-2.2.2.1409.jar
```

### 3. Restart the pod

```bash
kubectl rollout restart deployment <sonarqube-deployment>
```

---

## Verify Installation

After restart, go to **Administration > Marketplace > Installed** to confirm the plugin appears.

---

## Common Plugins

| Plugin | Description |
|--------|-------------|
| [sonar-cxx](https://github.com/SonarOpenCommunity/sonar-cxx) | C/C++ language support |
| [sonar-kotlin](https://github.com/SonarSource/sonar-kotlin) | Kotlin language support |
| [sonar-ansible](https://github.com/sbaudoin/sonar-ansible) | Ansible YAML linting |
| [sonar-dependency-check](https://github.com/dependency-check/dependency-check-sonar-plugin) | OWASP dependency vulnerability scanning |


# How to activate cxx

1. go to sonarqube ui
2. copy default profile to custom profile
    - Quality Profiles > filter by `cxx` > Sonar way 
    - 3dot > copy > entername > `cxx2`
3. set cxx2 as defaukt
    - Quality Profiles > filter by `cxx`
    - `cxx2` 3dot > set default