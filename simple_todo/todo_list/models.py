from django.contrib.auth.models import User
from django.db import models


# Data Model Classes
# ==================
class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todo_lists")
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.name} ({self.user})"


class Task(models.Model):
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=64, unique=True)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.todo_list})"
