# Lesson 08: Homepage

Now that we have created the data models we will need and registered them with the admin site, we can start creating the homepage for our website. The homepage for our website will display a form we can use to create a new todo list and a list of the todo lists which belong to the current user. To avoid having to reload the entire page when part of the content changes, we will use htmx. Let's start by modifying our `requirements.txt` file like this:
```
Django
django-allauth
django-environ
django-htmx
```

Now open a new terminal in Visual Studio code and execute the following command to install the new dependency:
```sh
pip install -r requirements.txt
```

Close the last terminal you opened. Then add "django_htmx" to the list of installed apps in `simple-todo/simple_todo/simple_todo/settings.py`:
```python
INSTALLED_APPS = [
    "layout",
    "accounts",
    "todo_lists",
    "allauth",
    "allauth.account",
    "django_htmx",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Next, we need to add the django_htmx middleware to the list of middleware in `simple-todo/simple_todo/simple_todo/settings.py`:
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
    "django_htmx.middleware.HtmxMiddleware"
]
```

Then download htmx by following the download instructions at https://htmx.org/docs/. Copy `htmx.min.js` to `simple-todo/simple_todo/layout/static/layout/js/`. Next, modify `simple-todo/simple_todo/layout/templates/layout/base.html` like this:
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>{{ WEBSITE_NAME }} - {% block title %}{% endblock %}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <link rel="stylesheet" href="{% static 'layout/css/bootstrap.min.css' %}"/>
        <script src="{% static 'layout/js/bootstrap.bundle.min.js' %}"></script>
        <script src="{% static 'layout/js/htmx.min.js' %}"></script>
    </head>
    <body>
        <div class="container-fluid">
            {% block content %}
            {% endblock %}
            <div class="row justify-content-center">
                <div class="col-8 m-2">Copyright (c) {% now 'Y' %} by {{ AUTHOR_NAME }}</div>
            </div>
        </div>
    </body>
</html>
```

At this point we haven't yet added our navigation bar to our main layout template. One way to add it would be to simply copy our navigation bar from the allauth base template. However, this would require duplicating code and be less maintainable. So instead, we will move our navigation bar code to a separate template and include it into the allauth base template and our main layout template. First we need to create `simple-todo/simple_todo/layout/templates/layout/navbar.html` with the following content:
```html
<div class="navbar navbar-expand-lg bg-body-tertiary border-bottom sticky-top">
    <div class="container-fluid">
        <a class="navbar-brand" href="/">{{ WEBSITE_NAME }}</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent" aria-controls="navbarContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                {% if not user.is_authenticated %}
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'account_signup' %}">Sign Up</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'account_login' %}">Sign In</a>
                    </li>
                {% else %}
                    <li class="nav-item">
                        <form action="{% url 'account_logout' %}" method="POST">
                            {% csrf_token %}
                            <input class="nav-link" type="submit" value="Logout"/>
                        </form>
                    </li>
                {% endif %}
            </ul>
        </div>
    </div>
</div>
```

Next we need to modify `simple-todo/simple_todo/accounts/templates/allauth/layouts/base.html` like this:
```html
{% load i18n %}
{% load static %}
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ WEBSITE_NAME }} - {% block head_title %}{% endblock head_title %}</title>
        <link rel="stylesheet" href="{% static 'layout/css/bootstrap.min.css' %}"/>
        <script src="{% static 'layout/js/bootstrap.bundle.min.js' %}"></script>
        {% block extra_head %}
        {% endblock extra_head %}
    </head>
    <body>
        {% block body %}
            {% include "layout/navbar.html" %}
            <div class="container-fluid">
                {% if messages %}
                    <div class="row justify-content-center">
                        <div class="col-8 m-2 alert alert-primary">
                            <strong>{% trans "Messages:" %}</strong>
                            <ul>
                                {% for message in messages %}<li>{{ message }}</li>{% endfor %}
                            </ul>
                        </div>
                    </div>
                {% endif %}
                <div class="row justify-content-center">
                    <div class="col-8 m-2 card bg-light">
                        <div class="card-body">
                            {% block content %}
                            {% endblock content %}
                        </div>
                    </div>
                </div>
            </div>
        {% endblock body %}
        {% block extra_body %}
        {% endblock extra_body %}
        <div class="row justify-content-center">
            <div class="col-8 m-2">Copyright (c) {% now 'Y' %} by {{ AUTHOR_NAME }}</div>
        </div>
    </body>
</html>
```

Then we need to modify `simple-todo/simple_todo/layout/templates/layout/base.html` like this:
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>{{ WEBSITE_NAME }} - {% block title %}{% endblock %}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <link rel="stylesheet" href="{% static 'layout/css/bootstrap.min.css' %}"/>
        <script src="{% static 'layout/js/bootstrap.bundle.min.js' %}"></script>
        <script src="{% static 'layout/js/htmx.min.js' %}"></script>
    </head>
    <body>
        {% include "layout/navbar.html" %}
        <div class="container-fluid">
            {% block content %}
            {% endblock %}
            <div class="row justify-content-center">
                <div class="col-8 m-2">Copyright (c) {% now 'Y' %} by {{ AUTHOR_NAME }}</div>
            </div>
        </div>
    </body>
</html>
```

Now we need to create the form we will need for creating new todo lists. Create `simple-todo/simple_todo/todo_lists/forms.py` with the following content:
```python
from django import forms

from .models import TodoList


# Form Classes
# ============
class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ["name"]
        widgets = {
            "name": forms.TextInput({"class": "form-control"})
        }
```

Form classes must extend either `forms.ModelForm` or `forms.Form`. If we use `forms.ModelForm` as the base class for a form, then the fields will automatically be generated based on the attributes of the inner `Meta` class. The `model` attribute of the inner meta class determines the data model class to use, the `fields` attribute of the inner meta class defines a list of fields to include on the form, and the optional `widgets` attribute of the inner meta class can be used to override the widget used for each field. Next create the following folder structure inside `simple-todo/simple_todo/todo_lists/`:
```
templates/
    todo_lists/
```

Then create `simple-todo/simple_todo/todo_lists/templates/todo_lists/todo_list_create_form.html` with the following content:
```html
<form hx-post="" hx-swap="outerHTML">
    {% csrf_token %}
    {{ form }}
    <br/>
    <button class="btn btn-primary">
        <div class="spinner-border spinner-border-sm htmx-indicator">
            <span class="visually-hidden">Loading...</span>
        </div>
        Create
    </button>
</form>
```

Since we're using htmx, we will use the `hx-post` attribute to define the URL to submit the form to. For now we will leave it blank so we can test the homepage more easily. The `hx-swap` attribute determines what content on the page will be replaced by the response. In this case, we will replace the entire form with the response. The progress spinner on the button has the "htmx-indicator" class added so it will only be visible while an AJAX request is in progress for the form containing the button. Next we need to create `simple-todo/simple_todo/todo_lists/templates/todo_lists/todo_lists_partial.html` with the following content:
```html
<div id="todo_lists-view">
    {% for todo_list in page_obj %}
        <div class="row">
            <div class="col m-1 card bg-light">
                <div class="card-body row">
                    <a class="col-10 nav-link" href="">{{ todo_list.name }}</a>
                    <button class="col-2 btn btn-danger" hx-delete="">Delete</button>
                </div>
            </div>
        </div>
    {% empty %}
        No Data
    {% endfor %}
    <br/>
    <div class="row justify-content-center">
        {% if page_obj.has_previous %}
            <button class="col-2 btn btn-primary"
                    hx-get="{% url 'todo-lists' %}?page={{ page_obj.previous_page_number }}"
                    hx-target="#todo_lists-view" 
                    hx-swap="outerHTML"
                    hx-push-url="true">
                    <div class="spinner-border spinner-border-sm htmx-indicator" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    Previous
            </button>
        {% else %}
            <button class="col-2 btn btn-secondary pe-none">Previous</button>
        {% endif %}
        <div class="col-2 text-center">Page {{ page_obj.number }} of {{ paginator.num_pages }}</div>
        {% if page_obj.has_next %}
            <button class="col-2 btn btn-primary"
                    hx-get="{% url 'todo-lists' %}?page={{ page_obj.next_page_number }}"
                    hx-target="#todo_lists-view"
                    hx-swap="outerHTML"
                    hx-push-url="true">
                    <div class="spinner-border spinner-border-sm htmx-indicator" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    Next
            </button>
        {% else %}
            <button class="col-2 btn btn-secondary pe-none">Next</button>
        {% endif %}
    </div>
</div>
```

The `hx-get` attribute determines what URL to fetch the previous/next page from, the `hx-target` attribute determines which element will be modified by the content fetched, and the `hx-swap` attribute determines how the target element will be modified. In this case, we will replace the entire element identified as "todo_lists-view" with the fetched content. The `hx-push-url` attribute is set to "true" in order to push the URL of the fetched content into the browser history. Now we need to create `simple-todo/simple_todo/todo_lists/templates/todo_lists/todo_lists_full.html` with the following content:
```html
{% extends "layout/base.html" %}

{% block title %}Todo Lists{% endblock %}

{% block content %}
    <div class="row justify-content-center">
        <div class="col-8 m-2 card bg-light">
            <div class="card-body">
                <h3 class="card-title">New Todo List</h3>
                {% include "todo_lists/todo_list_create_form.html" %}
            </div>
        </div>
    </div>
    <div class="row justify-content-center">
        <div class="col-8 m-2 card bg-light">
            <div class="card-body">
                <h3 class="card-title">Todo Lists</h3>
                {% include "todo_lists/todo_lists_partial.html" %}
            </div>
        </div>
    </div>
{% endblock %}
```

Next we need to create a view for our homepage. This view will need to be able to serve the full homepage, serve a new page of todo lists, and create a new todo list. To simplify this, we will create a separate view class for each task and then create a view which dispatches each request to the correct view based on the type of request. For now we will just implement serving the full homepage and a new page of todo lists. Open `simple-todo/simple_todo/todo_lists/views.py` and modify it like this:
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, View

from .forms import TodoListForm


# View Classes
# ============
class TodoListsFullView(ListView):
    template_name = "todo_lists/todo_lists_full.html"
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.todo_lists.order_by("name")
    
    def get_context_data(self, **kwargs):
        # Add the todo list form to the template context
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = TodoListForm()
        return ctx
    

class TodoListsPartialView(ListView):
    template_name = "todo_lists/todo_lists_partial.html"
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.todo_lists.order_by("name")
    

class TodoListsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Render partial content?
        if request.htmx:
            view = TodoListsPartialView.as_view()

        else:
            view = TodoListsFullView.as_view()

        return view(request, *args, **kwargs)
```

`TodoListsFullView` extends the `ListView` class. It renders the full homepage and provides automatic pagination for the todo lists owned by the current user. The `template_name` attribute determines which template will be rendered, the `paginate_by` attribute determines how many todo lists will be displayed per page, the `get_queryset` method returns the queryset of todo lists to be paginated, and the `get_context_data` method is used to add the todo list form to the template context. `TodoListsPartialView` extends the `ListView` class as well. It renders just the todo lists portion of the homepage and is therefore a bit simpler. `TodoListsView` extends `LoginRequiredMixin` and `View`. The `LoginRequiredMixin` will cause the user to be redirected to the login page if they aren't logged in. The `get` method uses the `htmx` attribute of the request to determine if the full page or partial page is being requested. Then it dispatches the request to the appropriate view and returns the response. Now we need to map our todo lists view to the URL for our homepage. Create `simple-todo/simple_todo/todo_lists/urls.py` with the following content:
```python
from django.urls import path

from . import views


urlpatterns = [
    path("", views.TodoListsView.as_view(), name="todo-lists")
]
```

Next, modify `simple-todo/simple_todo/simple_todo/urls.py` like this:
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
    path("", include("todo_lists.urls")),
    path("accounts/", include("accounts.urls")),
    path('admin/', admin.site.urls),
]
```

If you visit http://127.0.0.1:8000/ in your web browser, you will be redirected to the login page if you aren't already logged in. If you are logged in, you will see this page:
![homepage](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/12-homepage.png?raw=true)
