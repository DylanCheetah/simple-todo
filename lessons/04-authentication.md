# Lesson 04: Authentication

Our todo list will be multi-tenant. This means that multiple users will be able to create accounts and manage their todo lists. Therefore, we will need to create pages for users to register new accounts and log in. Django provides everything we need to create and manage user accounts, but it's up to us to create pages for user registration, login, etc. We can simplify the process by using django-allauth. Let's start by installing django-allauth. Open your `requirements.txt` file and modify it like this:
```
Django
django-allauth
django-environ
```

Next, open a new terminal in Visual Studo Code and execute the following command to install the new dependency:
```sh
pip install -r requirements.txt
```

Now you can close the last terminal you opened. The next thing we need to do is create an accounts app which will be used to manage user accounts. Execute the following command to create an accounts app:
```sh
python manage.py startapp accounts
```

Then we need to add the accounts app to the list of installed apps in `simple-todo/simple_todo/simple_todo/settings.py`. We also have to add a few apps provided by django-allauth:
```python
INSTALLED_APPS = [
    "layout",
    "accounts",
    "allauth",
    "allauth.account",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Next we need to add the django-allauth middleware to the list of middleware in `simple-todo/simple_todo/simple_todo/settings.py`:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]
```

We also need to add the following section to `simple-todo/simple_todo/simple_todo/settings.py`:
```python
# Authentication backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend"
]
```

Now we need to create a URL mapping for our accounts app. Create `simple-todo/simple_todo/accounts/urls.py` with the following content:
```python
from django.urls import include, path


urlpatterns = [
    path("", include("allauth.urls"))
]
```

Next, open `simple-todo/simple_todo/simple_todo/urls.py` and modify it like this:
```python
"""
URL configuration for simple_todo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path('admin/', admin.site.urls),
]
```

Then we need to execute the following command to apply migrations to our database. This will create the tables needed by all the installed apps:
```sh
python manage.py migrate
```

We also need to create a superuser account so we can test our new accounts app. Execute the following command and follow the prompts to create a superuser account:
```sh
python manage.py createsuperuser
```

If you visit http://127.0.0.1:8000/accounts/login/ you should see this page:
*screenshot*
