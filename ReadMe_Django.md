# Django
## Install Python

	install anaconda or install python
## Install Django
	conda install django
	# or
	pip install django
## Strat Project
#### create Project สร้างโปรเจค
	django-admin startproject <project name / ชื่อโปรเจค>
#### create app สร้างแอพ
	python manage.py startapp <app name / ชื่อแอพ>
  	# Edit in settings.py
	
	INSTALLED_APP = [
		... ,
		<app name>
	]
#
# DataBase
### ฐานข้อมูล
  	# Make migrations เตรียมสร้างฐานข้อมูล
	python manage.py makemigrations
	
	# สร้างฐานข้อมูล
	python manage.py migrate
# Run Server 
  	python manage.py runserver

# create admin
	python manage.py createsuperuser

