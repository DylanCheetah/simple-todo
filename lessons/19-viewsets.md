# Lesson 19: Viewsets

To create the structure of our REST API we will use viewsets. Each viewset class will manage one data model. Open `simple-todo/simple_todo/todo_lists_api_v1/views.py` and modify it like this:
```python
from django.shortcuts import render
from rest_framework import permissions, viewsets

from todo_lists.models import Task
from .serializers import TaskSerializer, TodoListSerializer


# ViewSet Classes
# ===============
class TodoListViewSet(viewsets.ModelViewSet):
    serializer_class = TodoListSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        return self.request.user.todo_lists.order_by("name")
    
    def perform_create(self, serializer):
        # Associate the new todo list with the current user
        serializer.save(user=self.request.user)
    

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        return Task.objects.filter(
            todo_list__user=self.request.user).order_by("name")
```

Each viewset class should extend the `viewsets.ModelViewSet` class. The `serializer_class` attribute determines which serializer to use, the `permission_classes` attribute determines which permission classes will be used to control access, and the `get_queryset` method should return a queryset of accessible data model instances. The `perform_create` method can be overridden to modify a data model instance before saving it. This is useful for associating a data model with the current user.
