# Lesson 15: Progressive Web App Project Setup

The first thing we need to do to setup our progressive web app is to create a REST API which will allow the frontend to fetch data from the backend. Django REST Framework greatly simplifies creating REST APIs. In order to use it we will first need to configure it though. Start by opening `simple_todo/simple_todo/settings.py` and modifying your list of installed apps like this:
```python
INSTALLED_APPS = [
    "todo_list",
    "accounts",
    "layout",
    "rest_framework",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Then add the following settings above your website constants:
```python
# REST framework
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10
}
```
