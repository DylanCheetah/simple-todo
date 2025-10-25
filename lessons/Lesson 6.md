# Lesson 6: User Registration

Since our todo list will be a multi-tenant web application we will need a way for users to create new accounts. At the moment, the only way we can create new accounts is by adding them via the admin site. However, many types of web applications need a way for users to create their own accounts without assistance from staff. For our todo list we will add an account registration page. Most websites will require an email address and do email verification. Having a CAPTCHA to help keep bots out is common as well. However, we will omit these to keep things simple. First we need to create a new "accounts" application to handle user registration for us:
```sh
python manage.py startapp accounts
```

Be sure to add the new accounts app to the list of installed apps in `simple_todo/simple_todo/settings.py`:
```python
INSTALLED_APPS = [
    "todo_list",
    "accounts",
    "layout",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Create a `simple_todo/accounts/templates/accounts` folder for your templates. Then create `simple_todo/accounts/templates/accounts/register.html` with the following content:
```html
{% extends 'layout/layout.html' %}

{% block title %}Register{% endblock %}

{% block content %}
    <div class="row justify-content-center">
        <h1 class="col-8">Register</h1>
    </div>
    <br/>
    <div class="row justify-content-center">
        <form class="col-8 card bg-light" method="POST">
            {% csrf_token %}
            <div class="card-body">
                {{ form }}
                <br/>
                <input class="btn btn-primary" type="submit" value="Register"/>
            </div>
        </form>
    </div>
{% endblock %}
```

`{% extends 'layout/layout.html' %}` will use our layout template for the page. Then we just need to insert content into the "title" and "content" blocks by redefining them with content inside. All forms must include `{% csrf_token %}` at the top to insert the token required by Django's CSRF middleware. And we insert the `form` context variable which will be populated with the registration form. Next we need to create our registration form. Create `simple_todo/accounts/forms.py` with the following content:
```python
from django import forms
from django.contrib.auth import forms as auth_forms


# Classes
# =======
class UserCreationForm(auth_forms.BaseUserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"})
        }

    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Apply Bootstrap styling to password fields
        self.fields["password1"].widget.attrs = {"class": "form-control"}
        self.fields["password2"].widget.attrs = {"class": "form-control"}
```

We can sub-class the `BaseUserCreationForm` provided by Django in order to create our own user creation form. Inside our `UserCreationForm` class we need to sub-class the inner class `Meta` and add a `widgets` dictionary to override the default widget used for the `username` field in order to add Bootstrap styling to it. Since both password fields are defined declaratively, we will need to also override the constructor and set the attributes of them manually after calling the base constructor. If we wanted to include additional fields, we would need to also override the `fields` attribute of the inner class `Meta` and possibly add additional fields declaratively. Now we can create our user registration view. Open `simple_todo/accounts/views.py` and modify it like this:
```python
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import UserCreationForm
from layout.views import LayoutMixin


# Classes
# =======
class UserCreateView(LayoutMixin, CreateView):
    template_name = "accounts/register.html"
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("user-login")
```

Our user registration view is simply a sub-class of `CreateView` and `LayoutMixin`. Make sure that `LayoutMixin` is first. We must specify the template name, model, and form class to use. And we need a URL to redirect to when a user account is successfully created. However, the logic for handling user account creation is handled by the view and form. Now we just need to map our new view to a URL. Create `simple_todo/accounts/urls.py` with the following content:
```python
from django.urls import path

from . import views


urlpatterns = [
    path("register/", views.UserCreateView.as_view(), name="user-create")
]
```

This will map our user creation view to the `register/` URL of our accounts app. We will also need to map our accounts app to a URL. Open `simple_todo/simple_todo/urls.py` and modify it like this:
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path('admin/', admin.site.urls),
]
```

Now if you visit [http://127.0.0.1:8000/accounts/register/](http://127.0.0.1:8000/accounts/register/) in a web browser you should see this page:
![user registration page](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/09-user_registation.png?raw=true)
