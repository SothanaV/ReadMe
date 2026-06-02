# Airflow v3: Configure OAuth Authentication

## Table of Contents

- [Prerequisites](#prerequisites)
- [OAuth Provider Registration](#oauth-provider-registration)
- [Configuration File](#configuration-file)
- [Mount the Config File](#mount-the-config-file)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Install the required packages:

```text
apache-airflow-providers-fab==2.4.2
Authlib==1.6.4
Flask-Limiter==3.12
```

---

## OAuth Provider Registration

Register your application with the OAuth provider and collect:

- **Client ID**
- **Client Secret**
- **Redirect URI** — must be in the format:

```text
http://<host>/auth/oauth-authorized/dsm
```

Example: `http://localhost:8080/auth/oauth-authorized/dsm`

---

## Configuration File

Create `webserver_config.py`:

```python
from __future__ import annotations

import os
import requests
from flask_appbuilder.security.manager import AUTH_OAUTH
from airflow.providers.fab.auth_manager.security_manager.override import FabAirflowSecurityManagerOverride

basedir = os.path.abspath(os.path.dirname(__file__))

# Flask-WTF CSRF protection
WTF_CSRF_ENABLED = True

AUTH_TYPE = AUTH_OAUTH
OAUTH_PROVIDERS = [
    {
        'name': 'dsm',
        'token_key': 'access_token',
        'icon': 'fa-lock',
        'remote_app': {
            'api_base_url': 'http://.../api/v1/account/me/',   # internal
            'access_token_url': 'http://.../o/token/',          # internal
            'authorize_url': 'https://.../o/authorize',         # external
            'request_token_url': None,
            'client_id': '...',
            'client_secret': '...',
        },
    }
]


class CustomSecurity(FabAirflowSecurityManagerOverride):

    def sync_roles(self):
        # Skip default role sync to use custom role assignment
        pass

    def get_oauth_user_info(self, provider, response=None):
        if provider == 'dsm':
            config = {}
            for elm in OAUTH_PROVIDERS:
                if elm.get('name') == 'dsm':
                    config = elm.get('remote_app')
            res = requests.get(config.get('api_base_url'), headers={
                'Authorization': f"{response.get('token_type')} {response.get('access_token')}"
            })
            if res.status_code != 200:
                print(res.text)
                return {}
            me = res.json()
            print(me)
            return {
                'email': me['email'],
                'first_name': me['first_name'],
                'last_name': me['last_name'],
                'username': me['username'],
                'role_keys': ['Admin', 'Viewer'],
            }
        return {}


SECURITY_MANAGER_CLASS = CustomSecurity
AUTH_USER_REGISTRATION = True
AUTH_ROLES_SYNC_AT_LOGIN = True
AUTH_USER_REGISTRATION_ROLE = 'Admin'
```

---

## Mount the Config File

### Docker Compose

```yaml
airflow-apiserver:
  image: my-airflow
  volumes:
    - ./logs:/opt/airflow/logs
    - ./config/webserver_config.py:/opt/airflow/webserver_config.py:ro
  ports:
    - "8080:8080"
  command: api-server
```

### Kubernetes

Add `webserver_config.py` to the `airflow-config` ConfigMap, then mount it in the API server Deployment:

```yaml
containers:
  - name: api-server
    # ...
    volumeMounts:
      # ...
      - name: config
        readOnly: true
        mountPath: /opt/airflow/webserver_config.py
        subPath: webserver_config.py
```

---

## Troubleshooting

### AttributeError: 'NoneType' object has no attribute 'name'

```text
File "/home/airflow/.local/lib/python3.12/site-packages/airflow/providers/fab/auth_manager/models/__init__.py", line 287, in perms
    (perm.action.name, perm.resource.name) for role in self.roles for perm in role.permissions
     ^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'name'
```

This error occurs when there are permission rows in the database with a `NULL` `permission_id`. Fix by deleting those orphaned rows:

```python
import pandas as pd
import psycopg2

con = "postgresql://postgres:postgres@airflow-postgresql.airflow:5432"

# Check for NULL permission rows
pd.read_sql_query("""
    SELECT * FROM ab_permission_view
    WHERE permission_id IS NULL
""", con)

# Delete the NULL rows
conn = psycopg2.connect(con)
cur = conn.cursor()
cur.execute("""
    DELETE FROM ab_permission_view
    WHERE permission_id IS NULL
""")
conn.commit()
```
