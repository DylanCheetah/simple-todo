# Lesson 17: Progressive Web App - Serializers

In lesson 3 we created data model classes for our todo list app. We will be using the same data model classes for our progressive web app. To use them with our REST API we will need a way to serialize data to be sent to our progressive web app and deserialize data received by our REST API. Django REST Framework handles this via serializer classes. Let's start by creating serializer classes for our todo list and task data model classes. Create `simple_todo/todo_list_api_v1/serializers.py` with the following content:
```python
from rest_framework import serializers

from todo_list.models import Task, TodoList


# Serializer Classes
# ==================
class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = ["id", "user", "name"]
        extra_kwargs = {
            "user": {"write_only": True}
        }


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "todo_list", "name", "due_date", "completed"]
```

Each serializer class needs to extend `ModelSerializer`. The `model` attribute of the inner `Meta` class determines which data model class will be used for serializing/deserializing data. The `fields` attribute of the inner `Meta` class will determine which fields will be serialized/deserialized. The `extra_kwargs` attribute of the inner `Meta` class can be used to specify additional options for each field.
