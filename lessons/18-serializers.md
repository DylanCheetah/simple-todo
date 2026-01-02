# Lesson 18: Serializers

Our REST API will need to be able to convert data models to JSON and convert JSON to data models. This is known as serialization and deserialization. We can handle this by creating serializer classes for our data models. Create `simple-todo/simple_todo/todo_lists_api_v1/serializers.py` with the following content:
```python
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
```

Each serializer extends the `serializers.ModelSerializer` class and defines an inner meta class. The `model` attribute of the inner meta class determines which data model to serialize/deserialize and the `fields` attribute determines which fields to use.
