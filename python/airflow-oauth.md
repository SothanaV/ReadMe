# Airflow config auth via Oauth

## edit `airflow-config.py`
```py
from __future__ import annotations

import os
import requests
from airflow.www.fab_security.manager import AUTH_OAUTH
from airflow.www.security import AirflowSecurityManager

basedir = os.path.abspath(os.path.dirname(__file__))

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True

AUTH_TYPE = AUTH_OAUTH
OAUTH_PROVIDERS = [{
    'name':'dsm',
    'token_key':'access_token',
    'icon':'fa-lock',
        'remote_app': {
            'api_base_url':'http://.../api/v1/account/me/',
            'access_token_url':'http://.../o/token/',
            'authorize_url':'https://.../o/authorize',
            'request_token_url': None,
            'client_id': "...",
            'client_secret': "...",
        }
}]


class CustomSecurity(AirflowSecurityManager):
    
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