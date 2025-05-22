from rest_framework.serializers import ModelSerializer

from .models import Task, TodoList


# Serializers
# ===========
class TodoListSerializer(ModelSerializer):
    class Meta:
        model = TodoList
        fields = ["url", "id", "name"]


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ["url", "id", "todo_list", "name", "due_date"]
