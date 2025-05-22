from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Task, TodoList
from .serializers import TaskSerializer, TodoListSerializer


# Viewset Classes
# ===============
class TodoListViewSet(ModelViewSet):
    serializer_class = TodoListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TodoList.objects.filter(owner=self.request.user).order_by("name")
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        todo_list = self.request.query_params.get("todo_list")

        if todo_list is not None:
            return Task.objects.filter(todo_list__owner=self.request.user, todo_list=todo_list).order_by("name")
        
        return Task.objects.filter(todo_list__owner=self.request.user).order_by("name")
