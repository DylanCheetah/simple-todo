from rest_framework import serializers

from todo_list.models import Task, TodoList


# Serializer Classes
# ==================
class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = ["user", "name"]
        extra_kwargs = {
            "user": {"write_only": True}
        }


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["todo_list", "name", "due_date", "completed"]
