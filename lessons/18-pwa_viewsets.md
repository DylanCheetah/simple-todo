# Lesson 18: Progressive Web App - Viewsets

In order to define our REST API we will need to create viewset classes. Each viewset class is used to perform CRUD operations on a class of data models. Open `simple_todo/todo_list_api_v1/views.py` and modify it like this:
```python
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from todo_list.models import Task
from .serializers import TaskSerializer, TodoListSerializer


# View Classes
# ============
class TodoListViewSet(ModelViewSet):
    serializer_class = TodoListSerializer
    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        return self.request.user.todo_lists.order_by("name")
    

class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        return Task.objects.filter(todo_list__user=self.request.user)
```

Each model viewset class must extend either `ModelViewSet` or `ReadOnlyModelViewSet` depending on whether the viewset should be read/write or read-only. The `serializer_class` attribute should be set to the serializer class to use. The `permission_classes` should be a list of permission classes to apply. The `get_queryset` method should return the queryset of data model instances which can be accessed by the viewset.
