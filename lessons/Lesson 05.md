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

Next, open `simple_todo/layout/views.py` and modify it like this:
```python
from django.conf import settings
from django.shortcuts import render


# Classes
# =======
class LayoutMixin(object):
    def get_context_data(self, **kwargs):
        # Get base context
        ctx = super().get_context_data(**kwargs)

        # Add layout context variables
        ctx["WEBSITE_NAME"] = settings.WEBSITE_NAME
        ctx["AUTHOR_NAME"] = settings.AUTHOR_NAME
        return ctx
```

The `LayoutMixin` class will be used to add the context variables required by our layout template so we won't have to keep adding them to every view we create for our website. It's `get_context_data` method calls the base method to get the original context. Then it adds `WEBSITE_NAME` and `AUTHOR_NAME` to it. Both values come from the `settings` module which we can import from `django.conf`.
