
# Play with Tamil - Backend

Django + Django REST Framework based LMS.


## Features
1. Authentication & Authorisation.
2. Manage user profile & credentials.
3. Create, browse and play activities.
4. Create users, zones
5. Invite/enroll users and play
6. Static pages

## Tech stack
1. Python 3.8
2. Django 3.2 LTS
3. Django REST Framework 3.12


## Installation

Install virtualenv & activate virtual environment
```sh
$ virtualenv venv
$ source venv/bin/activate
```

Install Django & required packages
```sh
(venv) $ pip install -r requirements.txt
```

## Database setup
Create database
```sh
CREATE DATABASE library;
make sure your username and password put database keyword in setting file
```

Migrate models & create superuser 
```sh
(venv) $ python manage.py makemigrations
(venv) $ python manage.py migrate
(venv) $ python manage.py createsuperuser
```

Run dev server in port 8000
```sh
(venv) $ python manage.py runserver
```

Make sure server running in port 8000 using below url in browser 
```sh
http://127.0.0.1:8000  (or)  http://yourip:8000  
```

For admin access use below url in browser
```sh
http://127.0.0.1:8000/admin/  (or)  http://yourip:8000/admin  
```