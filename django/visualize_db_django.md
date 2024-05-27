# Visuzlize database schema django

install graphviz
1. install native ubuntu/linux
```
sudo apt install graphviz
```

2. add this in Dockerfile

```dockerfile
...
RUN apt install -y graphviz
...
```

install packet
```
pip install django-extensions pydotplus
```

edit in settings.py
```
INSTALLED_APPS = [ 
    ...
    'django_extensions',
]
```

use
```
# all sechme
python manage.py graph_models -a -g -o <imagefile_name.png>

# some app
python manage.py graph_models <app1 app2> -o app1_app2.png
```
