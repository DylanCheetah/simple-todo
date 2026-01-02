# Lesson 20: Routers

Now that we have created the structure of our REST API, we need to map our viewsets to URLs. We can do this by using a router. The default router provided by Django REST Framework will automatically generate a set of URLs for each viewset we register. Open `simple-todo/simple_todo/todo_lists_api_v1/urls.py` and modify it like this:
```python
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from .views import TaskViewSet, TodoListViewSet


# Configure router
router = DefaultRouter()
router.register("todo-lists", TodoListViewSet, "todo_list")
router.register("tasks", TaskViewSet, "task")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls")),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh")
]
```

After we create an instance of the default router we call its `register` method with the base URL, viewset, and model name for each viewset we wish to register. Then we include the value of the `urls` attribute of our router into our URL config. When our website is in debug mode, we can view our REST API as a series of generated webpages by visiting the root URL of our REST API in a web browser. If you visit http://127.0.0.1:8000/api/v1/ in a web browser, you should see this page:
![rest api root](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/23-rest_api_root.png?raw=true)

The root page of the REST API shows the URL which each viewset was mapped to. If you visit http://127.0.0.1:8000/api/v1/todo-lists/ you should see this page:
![todo lists api](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/24-todo_lists_api.png?raw=true)

You can use the form at the bottom of the page to create a new todo list. If you add the ID of a todo list to the end of the current URL, you should see this page:
![todo list details api](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/25-todo_list_details_api.png?raw=true)

You can use the form at the bottom of the page to modify the todo list you're viewing. You can also click the delete button to delete the todo list you're viewing. Each viewset will have 2 URL endpoints which together provide 5 actions. The URL endpoints for the todo list viewset are:
```
GET    /api/v1/todo-lists/
POST   /api/v1/todo-lists/
GET    /api/v1/todo-lists/<pk:int>/
PUT    /api/v1/todo-lists/<pk:int>/
PATCH  /api/v1/todo-lists/<pk:int>/
DELETE /api/v1/todo-lists/<pk:int>/
```

We will use these URL endpoints and the task URL endpoints to manipulate data via our mobile app.
