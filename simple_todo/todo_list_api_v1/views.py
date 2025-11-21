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
        return Task.objects.filter(todo_list__user=self.request.user).order_by("name")
