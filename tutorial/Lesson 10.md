# Lesson 10: Create Account Registration Page

Now that we have completed the REST API for our todo list application, we need to setup a way for users to create new accounts, log in, and log out. Most web apps would also have features such as email verification, password reset, and account settings. However, for this tutorial we will just be implementing the bare mimimum to have a working account system. The first thing we need to do is create a new Django application called `accounts`. To do this, execute the following command:
```sh
python manage.py startapp accounts
```

Next, open `simple_todo/simple_todo/settings.py` and add the `accounts` app to the list of installed applications like this:
```python
INSTALLED_APPS = [
    "api",
    "accounts",
    "rest_framework",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Now we need to create the folders for our static files and page templates. Create the following folders:
`simple_todo/accounts/static/`
`simple_todo/accounts/static/accounts/`
`simple_todo/accounts/static/accounts/css/`
`simple_todo/accounts/templates/`
`simple_todo/accounts/templates/accounts`

Next we need to add Bootstrap to our accounts app. We will use it to help style our webpages. Download Bootstrap from [https://getbootstrap.com/](https://getbootstrap.com/). Then extract the .zip file and copy `bootstrap.min.css` to `simple_todo/accounts/static/accounts/css/`.

Now we need to create a registration form for new users. Create `simple_todo/accounts/forms.py` with the following content:
```python
from django import forms


# Forms
# =====
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=64, widget=forms.TextInput({"class": "form-control"}))
    password = forms.CharField(max_length=128, widget=forms.TextInput({"class": "form-control", "type": "password"}))
```

Then create `simple_todo/accounts/templates/accounts/layout.html` with the following content:
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>{% block title %}{% endblock %}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="{% static 'accounts/css/bootstrap.min.css' %}">
    </head>
    <body>
        {% block content %}
        {% endblock %}
    </body>
</html>
```

This HTML template will serve as the layout for all 3 account pages. It provides the basic skeleton of each webpage, loads the static files middleware, and loads the Bootstrap CSS file. Now we can create `simple_todo/accounts/templates/accounts/register.html` with the following content:
```html
{% extends "accounts/layout.html" %}

{% block title %}Simple Todo - Register{% endblock %}

{% block content %}
    <div class="container-fluid">
        <div class="row justify-content-center">
            <h1 class="col-10">Register</h1>
        </div>
        {% if err_msg %}
            <div class="row justify-content-center">
                <div class="col-10 alert alert-danger">{{ err_msg }}</div>
            </div>
        {% endif %}
        <div class="row justify-content-center">
            <div class="col-10 card text-bg-light">
                <form class="card-body" method="post">
                    {% csrf_token %}
                    {{ form }}
                    <input class="mt-2 btn btn-primary" type="submit" value="Register">
                </form>
            </div>
        </div>
    </div>
{% endblock %}
```

Next we will need to create a view for our registration page. Open `simple_todo/accounts/views.py` and modify it like this:
```python
from django.contrib.auth import login
from django.contrib.auth.models import AnonymousUser, User
from django.db import IntegrityError
from django.shortcuts import redirect, render

from .forms import RegistrationForm


# Views
# =====
def register(request):
    # Redirect automatically if already logged in
    if request.user.is_authenticated:
        url = request.GET.get("next", "/")
        return redirect(url)

    # Create registration form
    form = RegistrationForm()

    # Process submitted form data
    if request.method == "POST":
        # Validate form data
        form = RegistrationForm(request.POST)

        if form.is_valid():
            # Create user account
            try:
                user = User.objects.create_user(
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password"]
                )

            except IntegrityError:
                # Redisplay registration form
                return render(
                    request,
                    "accounts/register.html",
                    {
                        "err_msg": "The username you chose is already taken. Please choose a different username and try again.",
                        "form": RegistrationForm()
                    }
                )

            # Log in automatically
            login(request, user)

            # Redirect to the URL passed via the `next` query param
            url = request.GET.get("next", "/")
            return redirect(url)

    # Send account registration form
    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )
```

Create `simple_todo/accounts/urls.py` with the following content:
```python
from django.urls import path

from .views import register


# Create URL mappings
urlpatterns = [
    path("register/", register, name="account-register")
]
```

Open `simple_todo/simple_todo/urls.py` and modify it like this:
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/v1/", include("api.urls")),
    path("accounts/", include("accounts.urls")),
    path('admin/', admin.site.urls),
]
```

Now you should be able to execute `python manage.py runserver` and visit [http://localhost:8000/accounts/register/](http://localhost:8000/accounts/register/) to view the account registration form. If you are already logged in, you will be automatically redirected to the homepage by default. Use the admin site to log out first if this happens. You should see a page like this:
![image](https://github.com/user-attachments/assets/3ee8931a-d519-4d16-ac8a-1c3171cd8911)

If you attempt to register with an existing username, you will see this page:
![image](https://github.com/user-attachments/assets/ac4b240a-29ee-4d2c-b8fd-8b0ebc930f86)

For now, visiting the homepage should yield an error page like this:
![image](https://github.com/user-attachments/assets/a6e9c0a0-3207-4553-8fdf-2bc5505b5734)
