# Lesson 05: Page Layout and Bootstrap

Before we begin developing the web interface for our todo list, we need to setup the common layout all our pages will have and install Bootstrap. Let's start by creating a new app called "layout":
```sh
python manage.py startapp layout
```

Add "layout" to the list of installed apps in `simple_todo/settings.py`:
```python
INSTALLED_APPS = [
    "todo_list",
    "layout",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Now let's install Bootstrap. First, download the Boostrap compiled CSS and JS files from [https://getbootstrap.com/](https://getbootstrap.com/). You should have an archive containing the following folder structure where the "x" characters indicate the Bootstrap version:
```
bootstrap-x.x.x-dist/
    css/
    js/
```

Next, create a `static` folder inside the `simple_todo/layout` folder. Then create a `layout` folder inside the `simple_todo/layout/static` folder. Now we can copy the `css` and `js` folders from the bootstrap archive into the `simple_todo/layout/static/layout` folder. You should end up with the following project structure:
```
simple-todo/
    simple_todo/
        layout/
            migrations/
            static/
                layout/
                    css/
                    js/
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
        todo_list/
            migrations/
            __init__.py
            admin.py
            apps.py
            models.py
            tests.py
            views.py
        manage.py
    venv/
    requirements.txt
```

Now we need to create the template for our page layout. Create a `templates` folder inside `simple_todo/layout`. Then create a `layout` folder inside `simple_todo/layout/templates`. You should end up with the following project structure:
```
simple-todo/
    simple_todo/
        layout/
            migrations/
            static/
                layout/
                    css/
                    js/
            templates/
                layout/
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
        todo_list/
            migrations/
            __init__.py
            admin.py
            apps.py
            models.py
            tests.py
            views.py
        manage.py
    venv/
    requirements.txt
```

Now create `simple_todo/layout/templates/layout/layout.html` with the following content:
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>{{ WEBSITE_NAME }} - {% block title %}{% endblock %}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <link rel="stylesheet" href="{% static 'layout/css/bootstrap.min.css' %}"/>
        <script src="{% static 'layout/js/bootstrap.bundle.min.js' %}"></script>
    </head>
    <body>
        <div class="container-fluid">
            {% block content %}
            {% endblock %}
            <br/>
            <div class="row justify-content-center">
                <div class="col-8">
                    Copyright (c) {% now 'Y' %} by {{ AUTHOR_NAME }}
                </div>
            </div>
        </div>
    </body>
</html>
```

`{% load static %}` is used at the top of the template to load the `static` tag. Afterwards we have the basic structure which will be shared by our webpages. We use `{{ WEBSITE_NAME }}` to insert the value of the `WEBSITE_NAME` context variable into the title of the webpage. `{% block title %}{% endblock %}` will serve as a placeholder for the title of each individual page that we will insert via the template for each page. `{% static 'layout/css/bootstrap.min.css' %}` will insert the URL of the Bootstrap CSS file into the `href` attribute of the `link` element. `{% static 'layout/js/bootstrap.bundle.min.js' %}` will insert the URL of the Bootstrap JS file into the `src` attribute of the `script` element. `{% block content %}{% endblock %}` will server as a placeholder for the content of each page that we will insert via the template for each page as well. We use `{% now 'Y' %}` to insert the current year into the copyright info. And we use `{{ AUTHOR_NAME }}` to insert the value of the `AUTHOR_NAME` context variable into the copyright info. Next, we can test out our layout template. Execute `python manage.py shell` to start a Django shell. Then execute the following Python code in the Django shell:
```python
from django.template import loader
print(loader.render_to_string("layout/layout.html", {"WEBSITE_NAME": "Test", "AUTHOR_NAME": "Tester"}))
```

You should see the following HTML code printed to the terminal:
```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Test - </title>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <link rel="stylesheet" href="/static/layout/css/bootstrap.min.css"/>
        <script src="/static/layout/js/bootstrap.bundle.min.js"></script>
    </head>
    <body>
        <div class="container-fluid">


            <br/>
            <div class="row justify-content-center">
                <div class="col-8">
                    Copyright (c) 2025 by Tester
                </div>
            </div>
        </div>
    </body>
</html>
```

Type `exit()` to exit the Django shell. Then open `simple_todo/simple_todo/settings.py` and add the following section to the bottom of the file:
```python
# Website constants
WEBSITE_NAME = "Simple Todo"
AUTHOR_NAME = "DylanCheetah"
```

In order to make these 2 variable available via the template context of all views, we will need to create a context processor. Create `simple_todo/layout/ctx_proc.py` with the following content:
```python
from django.conf import settings


# Context Processor Functions
# ===========================
def layout_ctx(request):
    return {
        "WEBSITE_NAME": settings.WEBSITE_NAME,
        "AUTHOR_NAME": settings.AUTHOR_NAME
    }
```

The `layout_ctx` method returns a dictionary containing the context variables which should be made available to all views. We can import our settings module from `django.conf` to access the variables defined in it. To use our new context processor we must add its full name to the list of context processors in `simple_todo/simple_todo/settings.py`:
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
                "layout.ctx_proc.layout_ctx"
            ],
        },
    },
]
```
