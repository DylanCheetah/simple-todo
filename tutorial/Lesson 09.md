# Lesson 09: Create API Router

To map our viewsets to URL patterns, we will need to create a router, register our viewsets with it, and include the paths it generates into our URL configuration. To assist with testing, we will also include the REST framework URLs under the `auth/` base route. Create `simple_todo/api/urls.py` with the following content:
```python
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, TodoListViewSet


# Create router
router = DefaultRouter()
router.register("todo-lists", TodoListViewSet, "todolist")
router.register("tasks", TaskViewSet, "task")

# Define routes
urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls"))
]
```

Next we need to open `simple_todo/simple_todo/urls.py` and modify it like this:
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/v1/", include("api.urls")),
    path('admin/', admin.site.urls),
]
```

Afterwards, we can test our rest API by executing the following command:
```python
python manage.py test
```

If everything is working, all unit tests should pass. If there are any bugs, then one or more unit tests should fail. It is also possible for unit tests to fail if the tests themselves have bugs.
