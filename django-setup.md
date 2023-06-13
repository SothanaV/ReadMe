# Setup extra django
`settings.py`

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}
```

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'UPDATE_LAST_LOGIN':True
}
```

# Custom admin login
edit in `urls.py`
```python
from django.contrib import admin
...

admin.site.login_template = 'admin/custom-login.html'
admin.site.site_title = "Adhoc Import"
admin.site.site_header = "Adhoc Import"

...
urlpatterns = [
    path('admin/', admin.site.urls),
    ...
]
```
create file in `templates/admin/custom-login.html`

```html
{% extends "admin/base_site.html" %}
{% load i18n static %}

{% block extrastyle %}{{ block.super }}<link rel="stylesheet" href="{% static "admin/css/login.css" %}">
{{ form.media }}
{% endblock %}

{% block bodyclass %}{{ block.super }} login{% endblock %}

{% block usertools %}{% endblock %}

{% block nav-global %}{% endblock %}

{% block nav-sidebar %}{% endblock %}

{% block content_title %}{% endblock %}

{% block nav-breadcrumbs %}{% endblock %}

{% block content %}
{% if form.errors and not form.non_field_errors %}
<p class="errornote">
{% blocktranslate count counter=form.errors.items|length %}Please correct the error below.{% plural %}Please correct the errors below.{% endblocktranslate %}
</p>
{% endif %}

{% if form.non_field_errors %}
{% for error in form.non_field_errors %}
<p class="errornote">
    {{ error }}
</p>
{% endfor %}
{% endif %}

<div id="content-main">

{% if user.is_authenticated %}
<p class="errornote">
{% blocktranslate trimmed %}
    You are authenticated as {{ username }}, but are not authorized to
    access this page. Would you like to login to a different account?
{% endblocktranslate %}
</p>
{% endif %}

<form action="{{ app_path }}" method="post" id="login-form">{% csrf_token %}
  <div class="form-row">
    {{ form.username.errors }}
    {{ form.username.label_tag }} {{ form.username }}
  </div>
  <div class="form-row">
    {{ form.password.errors }}
    {{ form.password.label_tag }} {{ form.password }}
    <input type="hidden" name="next" value="{{ next }}">
  </div>
  {% url 'admin_password_reset' as password_reset_url %}
  {% if password_reset_url %}
  <div class="password-reset-link">
    <a href="{{ password_reset_url }}">{% translate 'Forgotten your password or username?' %}</a>
  </div>
  {% endif %}
  <div class="submit-row">
    <input type="submit" value="{% translate 'Log in' %}">
  </div>
</form>
<div class="form-row">
  <hr>
  <div class="form-row" style="text-align: center;">
    <a 
      class="submit-row" 
      style="text-align: center;"
      href="{% url 'social:begin' 'dsmauth' %}">
      Login with Oauth2
    </a>
  </div>
</div>
</div>
{% endblock %}
```