# Lesson 03: Site Layout

Before we start creating the pages that make up our website, we need to setup the layout resources which will be shared by multiple pages of our website. Let's start by creating a layout app which will hold these resources. Open a new terminal in Visual Studio Code. Then execute the following commands to create the layout app:
```sh
cd simple_todo
python manage.py startapp layout
```

We also need to add our layout app to the list of installed apps in `simple-todo/simple_todo/simple_todo/settings.py`:
```python
INSTALLED_APPS = [
    "layout",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Your project structure should look like this now:
```
simple-todo/
    simple_todo/
        layout/
            migrations/
            __init__.py
            admin.py
            apps.py
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
        manage.py
    venv/
    requirements.txt
```

Create the following folders inside `simple-todo/layout/`:
```
static/
    layout/
        css/
        js/
templates/
    layout/
```

We will be using Bootstrap for the theme of our website. So we will need to install it next. Download Bootstrap from https://getbootstrap.com/. Then extract the archive you downloaded. Copy the `css/bootstrap.min.css` file from the archive to `simple-todo/simple_todo/layout/static/layout/css/` and copy the `js/bootstrap.bundle.min.js` file from the archive to `simple-todo/simple_todo/layout/static/layout/js/`. Now create `simple-todo/simple_todo/layout/templates/layout/base.html` with the following content:
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>{{ WEBSITE_NAME }} - {% block title %}{% endblock %}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <link rel="stylesheet" href="{% static 'layout/css/bootstrap.min.css' %}"/>
        <script src="{% static 'layout/js/bootstrap.bundle.min.js' %}"></script>
    </head>
    <body>
        <div class="container-fluid">
            {% if messages %}
                <div class="row justify-content-center">
                    <div class="col-8 m-2 alert alert-primary">
                        <strong>Messages:</strong>
                        <ul>
                            {% for message in messages %}
                                <li>{{ message }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
            {% endif %}
            {% block content %}
            {% endblock %}
            <div class="row justify-content-center">
                <div class="col-8 m-2">Copyright (c) {% now 'Y' %} by {{ AUTHOR_NAME }}</div>
            </div>
        </div>
    </body>
</html>
```

We use the `load` Django template tag to load the static file middleware so we can use the `static` tag to generate URLs for our static files automatically. If there are any messages to display, we use a for loop to iterate over them and display them inside an alert above the main content. We use the `block` and `endblock` tags to define named blocks where we can insert content via templates that extend the layout template. We insert the value of the `WEBSITE_NAME` and `AUTHOR_NAME` template context variables into the title and copyright sections. We use the `now` tag to insert the current year into the copyright section as well. Your project structure should look like this now:
```
simple-todo/
    simple_todo/
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
        manage.py
    venv/
    requirements.txt
```

Since the website name and author name will be the same on all pages, we will define them as variables in our `simple-todo/simple_todo/simple_todo/settings.py` file:
```python
# Website constants
WEBSITE_NAME = "Simple Todo"
AUTHOR_NAME = "DylanCheetah"
```

Then we will create a context processor which will automatically add them to the template context for every page. Create `simple-todo/simple_todo/layout/ctx_proc.py` with the following content:
```python
from django.conf import settings


# Context Processor Functions
# ===========================
def layout(request):
    return {
        "WEBSITE_NAME": settings.WEBSITE_NAME,
        "AUTHOR_NAME": settings.AUTHOR_NAME
    }
```

To use our new context processor, add it to the list of context processors in `simple-todo/simple_todo/simple_todo/settings.py`:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "layout.ctx_proc.layout"
            ],
        },
    },
]
```

At this point you can test your layout template by using the Django shell. Execute the following command to start the Django shell:
```sh
python manage.py shell
```

Next, execute the following Python code in the Django shell:
```python
from django.http import HttpRequest
from django.template.loader import render_to_string

print(render_to_string("layout/base.html", request=HttpRequest()))
```

You should see output like this:
```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Simple Todo - </title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <link rel="stylesheet" href="/static/layout/css/bootstrap.min.css"/>
        <script src="/static/layout/js/bootstrap.bundle.min.js"></script>
    </head>
    <body>
        <div class="container-fluid">


            <div class="row justify-content-center">
                <div class="col-8 m-2">Copyright (c) 2025 by DylanCheetah</div>
            </div>
        </div>
    </body>
</html>
```

The website name, author name, year, and static URLs should be correctly inserted into the template. The title and content blocks should be empty for now. Execute the following command to exit the Django shell:
```python
exit()
```
