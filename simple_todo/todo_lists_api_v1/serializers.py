from rest_framework import serializers

from .models import Task, TodoList


# Serializer Classes
# ==================
class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = ["id", "name"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "todo_list", "name", "due_date"]
