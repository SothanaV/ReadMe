# SonarQube Plugins

## Install via the UI (Marketplace)

This method requires the SonarQube instance to have internet access and is available on the Community Build edition.

1. Log in as a System Administrator.
2. Navigate to **Administration > Marketplace**.
3. Use the search bar to find the plugin you need.
4. Click **Install**.
5. Once the download completes, a prompt will appear at the top of the page. Click **Restart** to apply the changes.

## Install via CLI (Manual / Air-Gapped)

Use this method when the SonarQube instance has no internet access or you need a specific plugin version.

### 1. Exec into the SonarQube Pod or Container

```bash
kubectl exec -it <sonarqube-pod> -- /bin/bash
```

### 2. Download and Install the Plugin

```bash
mkdir -p /opt/sonarqube/extensions/plugins
cd /opt/sonarqube/extensions/plugins

# Example: sonar-cxx plugin
curl -L -O https://github.com/SonarOpenCommunity/sonar-cxx/releases/download/cxx-2.2.2/sonar-cxx-plugin-2.2.2.1409.jar
```

### 3. Restart the Pod

```bash
kubectl rollout restart deployment <sonarqube-deployment>
```

## Verify Installation

After the restart, navigate to **Administration > Marketplace > Installed** to confirm the plugin appears in the list.

## Common Plugins

| Plugin | Description |
| ------ | ----------- |
| [sonar-cxx](https://github.com/SonarOpenCommunity/sonar-cxx) | C/C++ language support |
| [sonar-kotlin](https://github.com/SonarSource/sonar-kotlin) | Kotlin language support |
| [sonar-ansible](https://github.com/sbaudoin/sonar-ansible) | Ansible YAML linting |
| [sonar-dependency-check](https://github.com/dependency-check/dependency-check-sonar-plugin) | OWASP dependency vulnerability scanning |

## Activate a Plugin's Quality Profile (Example: sonar-cxx)

After installing the `sonar-cxx` plugin, activate it by creating and setting a default quality profile:

1. Go to **Quality Profiles** in the SonarQube UI.
2. Filter by `C++ (Community)` or `cxx` to find the built-in `Sonar way` profile.
3. Click the three-dot menu next to `Sonar way` and select **Copy**.
4. Enter a name for the new profile (for example, `cxx-custom`) and confirm.
5. Filter by `cxx` again, locate your new profile, click its three-dot menu, and select **Set as Default**.

The new profile will now be used for all projects analyzed with the C++ language.
