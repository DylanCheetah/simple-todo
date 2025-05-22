# Lesson 07: Create Model Serializers

In order to serialize/deserialize data for our REST API, we will need to create model serializers. Create `simple_todo/api/serializers.py` with the following content:
```python
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
        fields = ["url", "id", "todo_list", "name", "due_date", "completed"]
```

Each serializer has metadata that associates it with a data model and a list of fields which it will serialize/deserialize. Notice that we omit the `owner` field for the todo list serializer. We will set that field later via a viewset.
