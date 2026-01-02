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
