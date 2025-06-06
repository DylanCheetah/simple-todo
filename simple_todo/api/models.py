from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Utility Functions
# =================
def today():
    return timezone.now().date()


# Data Models
# ===========
class TodoList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name} ({self.owner.username})"


class Task(models.Model):
    todo_list = models.ForeignKey(
        TodoList, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    due_date = models.DateField(default=today)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.todo_list})"
