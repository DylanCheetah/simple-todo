# Lesson 02: Creating a Django Project

For our todo list application we will be using Django to implement the backend. First we need to install
Django. To keep track of the packages we are using, we will list them in `requirements.txt`. Then we will
be able to install all the packages via the Python package manager. Create `requirements.txt` with the
following content:
```txt
Django
```

Then execute the following command to install the packages:
```sh
pip install -r requirements.txt
```

Next we need to create a new Django project for our backend. Django project names can only contain letters,
numbers, and underscores. Execute the following command to create the Django project for our todo list
backend:
```sh
django-admin startproject simple_todo
```

This will create a new folder with the following structure:
```
simple_todo/
    simple_todo/
        __init__.py
        asgi.py
        settings.py
        urls.py
        wsgi.py
    manage.py
```

Now we need to initialize the database for our application. Execute the following command to create a new
database and intialize it:
```sh
python manage.py migrate
```

We also need to create a superuser for the admin site. To do this, execute `python manage.py createsuperuser`
and follow the prompts.
