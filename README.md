# Getting Started Guide 
This document is a guide to creating a new django project that uses:
1. Ubuntu/Mac
2. python3.8.2
3. pip
4. django 2.2.15 (LTS)
5. virtualenv
6. Redis
7. django channels 2
8. Postgres

## Install Python3.8.2
Bottom of page: https://www.python.org/downloads/release/python-382/

## Installing pip
1. https://pypi.org/project/pip/
2. Open terminal
3. `pip install pip`

## Setup virtualenv
1. Navigate to where you want to keep your django projects. I use `Desktop/DjangoProjects/`
2. Create `Desktop/DjangoProjects/ChatApp` folder or whatever you want to name the project.
3. Create a virtual environment to run the project in.
	- `python -m venv dev`
4. Open a Terminal window in your project directly
5. Navigate into `ChatApp` folder
6. Activate the virtual environment
	- **Linux**: `source dev/bin/activate`
	- **Mac**: `source dev/bin/activate`


## Install Django and other Requirements
1. Install requirements
	- pip install -r requirements.txt


## Postgres Setup (Mac/Ubuntu)
Postgres needs to run as a service on your machine. 
1. Download postgres: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

2. run the installer file and go through the installation
	1. **remember the superuser password you use.** This is very important.
	2. port 5432 is the standard
3. After installation confirm the service is running.
	- If it's not running then start it
4. Confirm you have access to database
	1. open terminal
	2. write `psql postgres postgres`
		- means: "connect to the database named 'postgres' with the user 'postgres'". 'postgres' is the default root user name for the database.
		- use the password you have created while installing Postgresql
5. Some commands you'll find useful:
	1. List databases
		- `\l`
	2. create a new database for our project
		- `CREATE DATABASE chatapp_dev;`
	3. Create a new user that has permissions to use that database
		- `CREATE USER chatapp_admin WITH PASSWORD 'root@123';`
		- These credentials are important to remember because they are used in the django postgres configuration.
	4. List all users
		- `/du`
	5. Give the new user all privileges on new db
		- `GRANT ALL PRIVILEGES ON DATABASE chatapp_dev TO chatapp_admin;`
	6. Test
		1. disconnect from db
			- `\q`
		2. Connect to the db with user
			- `psql chatapp_dev chatapp_admin`


## Django and Postgres Setup (Already setup done)

1. Update `settings.py` with the following postgres configuration
	```
	DB_NAME = "chatapp_dev"
	DB_USER = "chatapp_admin"
	DB_PASSWORD = "root@123"
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.postgresql_psycopg2',
	        'NAME': DB_NAME,
	        'USER': DB_USER,
	        'PASSWORD': DB_PASSWORD,
	        'HOST': 'localhost',
	        'PORT': '5432',
	    }
	}
	```
2. Delete the sqlite database in project root
3. migrate to commit changes to database
	- `python manage.py migrate`
4. create a superuser
	- `python manage.py createsuperuser`
5. log into admin
	- `python manage.py runserver`
	- visit `http://127.0.0.1:8000/admin`
	- This confirms the database is working correctly.


## Install Redis (Required for Django Channels)(Already setup done)
1. Just download Redis the executable and run it.
2. Update settings with `CHANNEL_LAYERS` configuration
	```
	CHANNEL_LAYERS = {
	    'default': {
	        'BACKEND': 'channels_redis.core.RedisChannelLayer',
	        'CONFIG': {
	            "hosts": [('127.0.0.1', 6379)],
	        },
	    },
	}
	```


## Django Channels setup
Follow https://channels.readthedocs.io/en/latest/installation.html
1. Add channels to installed apps
	```
	INSTALLED_APPS = (
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.sites',
	    ...
	    'channels',
	)
	```
2. create default routing file `ChatServerPlayground/routing.py`
	```
	from channels.auth import AuthMiddlewareStack
	from channels.routing import ProtocolTypeRouter, URLRouter
	from channels.security.websocket import AllowedHostsOriginValidator
	from django.urls import path
	application = ProtocolTypeRouter({
		'websocket': AllowedHostsOriginValidator(
			AuthMiddlewareStack(
				# URLRouter([...]) # Empty for now because we don't have a consumer yet.
			)
		),
	})
	```

3. set your ASGI_APPLICATION in `settings.py`
	```
	ASGI_APPLICATION = "ChatServerPlayground.routing.application"
	```
4. Now you create Consumers and add to the `URLRouter` list.

## References
1. https://docs.djangoproject.com/en/2.2/
2. https://www.python.org/downloads/release/python-380/
3. https://realpython.com/getting-started-with-django-channels/
4. https://www.geeksforgeeks.org/what-is-web-socket-and-how-it-is-different-from-the-http/
5. https://www.youtube.com/watch?v=F4nwRQPXD8w
6. https://www.youtube.com/watch?v=8ARodQ4Wlf4
7. https://www.youtube.com/watch?v=u4kr7EFxAKk
8. https://www.youtube.com/watch?v=8hxr3T5cUbo
9. https://www.youtube.com/watch?v=R4-XRK6NqMA
10. https://www.youtube.com/watch?v=AZNp1CfOjtE
11. https://channels.readthedocs.io/en/stable/
12. https://www.section.io/engineering-education/building-chat-application-with-django-channel/
13. https://dev.to/earthcomfy/django-channels-a-simple-chat-app-part-2-eh9
14. https://djangopackages.org/grids/g/chat/
15. https://codewithstein.com/django-realtime-chat-app-tutorial-simple-django-tutorial-with-channels-and-redis/
