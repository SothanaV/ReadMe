# Move docker volume path to other path
reference https://www.guguweb.com/2019/02/07/how-to-move-docker-data-directory-to-another-location-on-ubuntu/
- Stop the docker daemon
```
sudo service docker stop

```

- Add a configuration file to tell the docker daemon what is the location of the data directory ```/etc/docker/daemon.json```

```
{ 
   "data-root": "/path/to/your/docker" 
}
```

- Copy the current data directory to the new one
```
sudo rsync -aP /var/lib/docker/ /path/to/your/docker
```

- Rename the old docker directory
```
sudo mv /var/lib/docker /var/lib/docker.old
```

- start docker daemon
```
sudo service docker start
```

- Test up docker
- remove old dockerfile
```
sudo rm -rf /var/lib/docker.old
```