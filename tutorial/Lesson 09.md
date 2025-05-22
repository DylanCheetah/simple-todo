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

At this point, you should be able to test the REST API manually as well by executing `python manage.py runserver` and visiting [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/) in a web browser. The homepage of the REST API will list the available APIs:
![image](https://github.com/user-attachments/assets/55ad437b-fe3f-46f2-adf2-a852c0cfea2e)

If you click one of the API links you should see the page for that particular API:
![image](https://github.com/user-attachments/assets/0b7a86dc-74dc-4c8b-9ac5-bbb52695225a)

Since we designed our APIs to only be accessible to authenticated users, you will need to use the login link in the upper right corner to log in. Afterwards, you will be able to access the API:
![image](https://github.com/user-attachments/assets/c6786e6f-1e6c-496a-9788-846e3d1262f8)

Each API supprts all CRUD operations:
![image](https://github.com/user-attachments/assets/d95de390-0ed8-4325-b7f5-efb405d4d213)
