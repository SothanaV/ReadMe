# Docker

$ sudo docker run -it --rm -v $(pwd):/code django bash
$ cd code
$ django-admin startproject [Nameproject]
$ exit
$ cd [project]
Edit in
	Setting.py => Edit  add in Install_app	//Add app Name
$ cd /home
$ sudo docker run -t --rm -p 0.0.0.0:5001:5000 -v $(pwd):/code -w /code/naii django python manage.py runserver 0.0.0.0:5000
$ sudo docker build .
$ sudo docker images
$ sudo docker run -it -p 0.0.0.0:5001:8000 [KEY]
$ sudo docker-compose up
------------------------------
$ sudo docker ps
$ sudo docker stop [name]
$ sudo docker rm [name]
-----------------------------