# Lesson 3: Setup Django REST Framework

We will be using Django REST Framework to help implement the REST API for our todo list app. To use it, we will need to install and configure it. First, modify your `requirements.txt` file like this:
```txt
Django
djangorestframework
```

Then execute `pip install -r requirements.txt` to install the additional package.

Open `simple_todo/simple_todo/settings.py` and add `rest_framework` to the top of the list of installed apps like this:
```python
INSTALLED_APPS = [
    "rest_framework",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Then add this to the bottom of the file:
```python
# REST Framework
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
	"PAGE_SIZE": 10,
	"DEFAULT_AUTHENTICATION_CLASSES": [
	    "rest_framework.authentication.SessionAuthentication"
	]
}
```
