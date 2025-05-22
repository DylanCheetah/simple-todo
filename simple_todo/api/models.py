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
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.todo_list})"
