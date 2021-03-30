# setup server
- install docker
```
$ sudo apt update
$ sudo apt install apt-transport-https ca-certificates curl software-properties-common
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
$ sudo apt update
$ sudo apt install docker-ce
$ sudo systemctl status docker
$ sudo groupadd docker
$ sudo usermod -aG docker ${USER}
$ newgrp docker 
$ id -nG
$ docker --version
$ docker run hello-world
```
- install docker-compose
```
$ sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
$ docker-compose --version
```

- install ctop
```
$ echo "deb http://packages.azlux.fr/debian/ buster main" | sudo tee /etc/apt/sources.list.d/azlux.list
$ wget -qO - https://azlux.fr/repo.gpg.key | sudo apt-key add -
$ sudo apt update
$ sudo apt install docker-ctop
```