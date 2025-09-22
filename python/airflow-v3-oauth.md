# Airflow config auth via Oauth
1. register application on oauth
    - create app
    - get app id
    - get app secret
    - redirect uri
        - ` http://<host>/auth/oauth-authorized/dsm` eg http://localhost:8080/auth/oauth-authorized/dsm

2. add `webserver_config.py`
```py
from __future__ import annotations

import os
import requests
from flask_appbuilder.security.manager import AUTH_OAUTH
from airflow.providers.fab.auth_manager.security_manager.override import FabAirflowSecurityManagerOverride

basedir = os.path.abspath(os.path.dirname(__file__))

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True

AUTH_TYPE = AUTH_OAUTH
OAUTH_PROVIDERS = [{
    'name':'dsm',
    'token_key':'access_token',
    'icon':'fa-lock',
        'remote_app': {
            'api_base_url':'http://.../api/v1/account/me/', # internal
            'access_token_url':'http://.../o/token/', # internal
            'authorize_url':'https://.../o/authorize', # external
            'request_token_url': None,
            'client_id': "...",
            'client_secret': "...",
        }
}]


class CustomSecurity(FabAirflowSecurityManagerOverride):
    
    def sync_roles(self):
        # Custom logic or possibly skipping the sync altogether
        pass

    def get_oauth_user_info(self, provider, response=None):
        if provider == "dsm":
            config = {}
            for elm in OAUTH_PROVIDERS:
                if elm.get('name') == 'dsm':
                    config = elm.get('remote_app')
            res = requests.get(config.get('api_base_url'), headers={
                'Authorization': f"{response.get('token_type')} {response.get('access_token')}"
            })
            if res.status_code!=200:
                print(res.text)
                return {}
            me = res.json()
            print(me)
            parsed_token = {
                "email": me["email"],
                "first_name": me["first_name"],
                "last_name": me["last_name"],
                "username": me["username"],
                "role_keys": ["Admin", "Viewer"],
            }
            return parsed_token
        return {}

SECURITY_MANAGER_CLASS = CustomSecurity
AUTH_USER_REGISTRATION = True
AUTH_ROLES_SYNC_AT_LOGIN = True
AUTH_USER_REGISTRATION_ROLE = "Admin"
```

3. mapping to api-server

    3.1 docker
    ```yml
    ...
    airflow-apiserver:
        image: my-airflow
        volumes:
            - ./logs:/opt/airflow/logs
            - ./config/webserver_config.py:/opt/airflow/webserver_config.py:ro
        ports:
            - "8080:8080"
        command: api-server
    ```

    3.2 k8s
    - add `webserver_config.py` in config map `airflow-config` 
    - update airflow-api-server deployment
    ```yml
    containers:
        - name: api-server
    ...
    volumeMounts:
           ...
        - name: config
            readOnly: true
            mountPath: /opt/airflow/webserver_config.py
            subPath: webserver_config.py
    ```