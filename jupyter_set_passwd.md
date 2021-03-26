# set jupyter password
## 1 create configfile
create jupyter_notebook_config.json

```
{
    "NotebookApp": {
      "password": "<PASSWORD>"
    }
}
```

## 2 create password

```
>>> from notebook.auth import passwd
>>> passwd()
Enter password: 
Verify password: 
'<PASSWORD>'
```

## 3 copy password to cfg file

## 4 settings to docker-compose

```
...
volumes: 
    ...
    - ./jupyter_notebook_config.json:/config/jupyter_notebook_config.json
    ...
```

## set command
```
jupyter notebook --allow-root --no-browser --ip=* --config=/config/jupyter_notebook_config.json
```
