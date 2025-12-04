from django.contrib.auth.models import User
from django.db import models


# Data Model Classes
# ==================
class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todo_lists")
    name = models.CharField(max_length=64)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                "user",
                "name",
                name="unique_user_name"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.user})"


class Task(models.Model):
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=64)
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False, verbose_name="complete")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                "todo_list",
                "name",
                name="unique_todo_list_name"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.todo_list})"
