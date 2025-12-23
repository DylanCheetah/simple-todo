# Lesson 17: REST API Setup

Before we start developing the mobile app for our project we will need to first setup a REST API which will allow our mobile app to communicate with our website. Open `requirements.txt` and modify it like this:
```
Django
django-allauth
django-environ
django-htmx
djangorestframework
djangorestframework-simplejwt
```

Next, open a new terminal in Visual Studio Code and execute the following command to install the new dependencies:
```sh
pip install -r requirements.txt
```

Then open `simple-todo/simple_todo/settings.py` and modify the list of installed apps like this:
```python
INSTALLED_APPS = [
    "layout",
    "accounts",
    "todo_lists",
    "allauth",
    "allauth.account",
    "django_htmx",
    "rest_framework",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

You also need to add the following section to `settings.py`:
```python
# REST framework
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ]
}
```

Now we need to create a new app for our REST API by executing the following commands:
```sh
cd simple_todo
python manage.py startapp todo_lists_api_v1
```

And we need to add it to our list of installed apps as well:
```python
INSTALLED_APPS = [
    "layout",
    "accounts",
    "todo_lists",
    "todo_lists_api_v1",
    "allauth",
    "allauth.account",
    "django_htmx",
    "rest_framework",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Next we need to create `simple-todo/simple_todo/todo_lists_api_v1/urls.py` with the following content:
```python
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path("auth/", include("rest_framework.urls")),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh")
]
```

This will configure the views needed for authentication with the REST API. We also need to include the URLs for our REST API into the main URL config by modifying `simple-todo/simple_todo/simple_todo/urls.py` like this:
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
    path("api/v1/", include("todo_lists_api_v1.urls")),
    path('admin/', admin.site.urls),
]
```
