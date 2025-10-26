# Lesson 07: User Authentication

Another important feature of a multi-tenant web application is user authentication. In order to provide this feature to users, we will need to create log in and log out views. Let's start by creating a template for our login page:
```html
{% extends 'layout/layout.html' %}

{% block title %}Login{% endblock %}

{% block content %}
    <div class="row justify-content-center">
        <h1 class="col-8">Login</h1>
    </div>
    <br/>
    <div class="row justify-content-center">
        <form class="col-8 card bg-light" method="POST">
            {% csrf_token %}
            <div class="card-body">
                {{ form }}
                <br/>
                <input class="btn btn-primary" type="submit" value="Login"/>
            </div>
        </form>
    </div>
{% endblock %}
```

The login page template will receive the `form` context variable which contains the user authentication form. Next we need to create our user authentication form. Open `simple_todo/accounts/forms.py` and modify it like this:
```python
from django import forms
from django.contrib.auth import forms as auth_forms


# Classes
# =======
class UserCreationForm(auth_forms.BaseUserCreationForm):
    class Meta(auth_forms.BaseUserCreationForm.Meta):
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"})
        }

    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Apply Bootstrap styling to password fields
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


class UserAuthenticationForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Apply Bootstrap styling to username and password fields
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["password"].widget.attrs.update({"class": "form-control"})
```

Our `UserAuthenticationForm` class should sub-class the `AuthenticationForm` provided by Django. Both the `username` and `password` fields are created declaratively, so we need to update their attributes via a custom constructor. Now we can create our login view. Open `simple_todo/accounts/views.py` and modify it like this:
```python
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import UserAuthenticationForm, UserCreationForm
from layout.views import LayoutMixin


# Classes
# =======
class UserCreateView(LayoutMixin, CreateView):
    template_name = "accounts/register.html"
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("user-login")


class UserLoginView(LayoutMixin, LoginView):
    template_name = "accounts/login.html"
    authentication_form = UserAuthenticationForm
```

Our `UserLoginView` class must sub-class `LoginView` and `LayoutMixin`. Make sure that `LayoutMixin` is first. We must specify the template name and authentication form to use. This view will handle the logic for logging in a user. We also need to open `simple_todo/simple_todo/settings.py` and add `LOGIN_REDIRECT_URL` to the website constants section. This will be the default URL the login view redirects to upon success:
```python
# Website constants
from django.urls import reverse_lazy

WEBSITE_NAME = "Simple Todo"
AUTHOR_NAME = "DylanCheetah"
LOGIN_REDIRECT_URL = reverse_lazy("todo-lists")
```

Now we need to map our login view to a URL. Open `simple_todo/accounts/urls.py` and modify it like this:
```python
from django.urls import path

from . import views


urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="user-login"),
    path("register/", views.UserCreateView.as_view(), name="user-create")
]
```

If you visit [http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/) in a web browser, you should see this page:
![user login page](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/10-user_login.png?raw=true)

We also need to add our log out view. The log out view doesn't need a template though. Open `simple_todo/accounts/views.py` and modify it like this:
```python
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import UserAuthenticationForm, UserCreationForm
from layout.views import LayoutMixin


# Classes
# =======
class UserCreateView(LayoutMixin, CreateView):
    template_name = "accounts/register.html"
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("user-login")


class UserLoginView(LayoutMixin, LoginView):
    template_name = "accounts/login.html"
    authentication_form = UserAuthenticationForm


class UserLogoutView(LogoutView):
    pass
```

The `UserLogoutView` doesn't need to define any additional attributes for our application. However, we do need to define the default URL it should redirect to in `simple_todo/simple_todo/settings.py`:
```python
# Website constants
from django.urls import reverse_lazy

WEBSITE_NAME = "Simple Todo"
AUTHOR_NAME = "DylanCheetah"
LOGIN_REDIRECT_URL = reverse_lazy("todo-lists")
LOGOUT_REDIRECT_URL = reverse_lazy("todo-lists")
```

And we also need to map our log out view to a URL. Open `simple_todo/accounts/urls.py` and modify it like this:
```python
from django.urls import path

from . import views


urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="user-login"),
    path("logout/", views.UserLogoutView.as_view(), name="user-logout"),
    path("register/", views.UserCreateView.as_view(), name="user-create")
]
```

If you visit [http://127.0.0.1:8000/accounts/logout/](http://127.0.0.1:8000/accounts/logout/) in a web browser, you will get a 405 Method Not Allowed error page for now. This is because the log out view only supports the "POST" HTTP method:
![user logout error page](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/11-user_logout_error.png?raw=true)

We will add a log out form in a later lesson.
