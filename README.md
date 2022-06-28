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

## Flow the ChatApp Project (After above steps once the server is up and running)
1. User needs to register an account 
2. User needs to login with the same credentials
3. Second user can register an account
4. Second user can also login with its credentials
5. From 1st user dashboard he can search the 2nd user
6. After the search he can send the friend request to 2nd user
7. 2nd user can accept the friend request of 1st user
8. After accepting the friend request both users became friends
9. In the account section friends tab is available with the recent added friend
10. Goto to the friend tab and click on message button
11. After clicking on message button the one to one private chat window will come and there both the users can chat
12. On the home screen the public chat window is available for chatting publicly
13. Screenshots have been kept inside "ChatApp_dev/static/screenshots" path for the reference

## Different way you can authenticate the web socket in Django
1. Session Authentication :
	If you authenticate your users, Django will create a session to track authenticated users and will assign a session variable to them. This session value will be sent to client-side via set-cookie header in response. And browser will save it, So all other requests will include this header by default. Even web-socket requests to django-channels.

2. Token Authentication (provide token in HTTP header) :
	If the Authorization token is provided in header of HTTP requests, then you can create a custom Authentication Middleware, So that it intercepts requests coming with web-socket to django-channels routers.This Middleware, will check keys provided in HTTP header. If authorization is sent, will try to fetch it’s value. If the token name is Token then will try to find the corresponded Token Object for this in database. If so will fetch the user for that and update scope['user'] with that value.

3. Token Authentication (No HTTP header required) : 
	Whenever a socket is created between client-side and django-channels, Until the token is not provided in first request of user in socket’s data, and that token is not valid; No other data will be transferred between them.


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
16. https://reza-ta.medium.com/django-channels-web-socket-authentication-approaches-3a56954b4120
