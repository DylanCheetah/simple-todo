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

We also need to add the following sections to `simple-todo/simple_todo/simple_todo/settings.py`:
```python
# Authentication backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend"
]

# Authentication URLs
LOGIN_REDIRECT_URL = "/"
```

django-allauth doesn't provide a page for deleting the current user's account, so we will need to create our own. Create a `simple-todo/simple_todo/accounts/templates/accounts/` folder. Your project structure should look like this now:
```
simple-todo/
    simple_todo/
        accounts/
            migrations/
            templates/
                accounts/
            __init__.py
            admin.py
            apps.py
            models.py
            tests.py
            urls.py
            views.py
        layout/
            migrations/
            static/
                layout/
                    css/
                        bootstrap.min.css
                    js/
                        bootstrap.bundle.min.js
            templates/
                layout/
                    base.html
            __init__.py
            admin.py
            apps.py
            ctx_proc.py
            models.py
            tests.py
            views.py
        simple_todo/
            __init__.py
            asgi.py
            settings.py
            urls.py
            wsgi.py
        .env
        .env.dist
        db.sqlite
        manage.py
    venv/
    requirements.txt
```

Then create `simple-todo/simple_todo/accounts/templates/accounts/account_delete.html` with the following content:
```html
{% extends "layout/base.html" %}

{% block title %}Delete Account{% endblock %}

{% block content %}
    <div class="row justify-content-center">
        <form class="col-lg-8 col-md-10 col-11 m-2 card bg-light"
              action="{% url 'account-delete' %}"
              method="POST">
            {% csrf_token %}
            <div class="card-body">
                <p>Are you sure you wish to <strong>permanently</strong> delete your account?</p>
                <div class="row justify-content-center">
                    <button class="col-5 m-1 btn btn-danger">Yes</button>
                    <a class="col-5 m-1 btn btn-primary" href="{% url 'todo-lists' %}">No</a>
                </div>
            </div>
        </form>
    </div>
{% endblock %}
```

This page has a form which asks the user to confirm if they want to delete their account. If they click Yes, their account will be deleted. If they click No, they will be redirected to the homepage. Next we need to create a view for the account deletion page. Open `simple-todo/simple_todo/accounts/views.py` and modify it like this:
```python
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView


# View Classes
# ============
class AccountDeleteView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/account_delete.html"

    def post(self, *args, **kwargs):
        # Delete the current user's account and return to the homepage
        self.request.user.delete()
        messages.add_message(
            self.request, 
            messages.INFO, 
            "Your account has been successfully deleted."
        )
        return HttpResponseRedirect(reverse("todo-lists"))
```

`AccountDeleteView` extends `LoginRequiredMixin` and `TemplateView`. The `template_name` attribute determines which template will be rendered when the view receives an HTTP GET request. We define a `post` method which will be called when the view receives and HTTP POST request. The `post` method will delete the current user, add a message indicating the user's account was successfully deleted, and redirect to the homepage. Now we need to create a URL mapping for our accounts app. Create `simple-todo/simple_todo/accounts/urls.py` with the following content:
```python
from django.urls import include, path

from . import views


urlpatterns = [
    path("", include("allauth.urls")),
    path("delete/", views.AccountDeleteView.as_view(), name="account-delete")
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
![default user login](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/02-default_user_login.png?raw=true)
