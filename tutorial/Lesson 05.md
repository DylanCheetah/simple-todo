# Lesson 05: Create Data Models

To manage the data used by our application, we will need to create data models. For this application, we will need 2 data models. One for todo lists and one for tasks. We will also use the user data model provided by Django. Open `simple_todo/api/models.py` and modify it like this:
```python
from django.contrib.auth.models import User
from django.db import models


# Data Models
# ===========
class TodoList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name} ({self.owner.username})"


class Task(models.Model):
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    due_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.todo_list})"
```

Next we need to create migrations and apply them to the database by executing the following commands:
```sh
python manage.py makemigrations
python manage.py migrate
```
