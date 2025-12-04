# Lesson 06: Data Models

In order to store the data for each user's todo lists, we will need to create data model classes. A data model class is used to manage a table of data in the database used by our Django project. Each data model class is defined within the `models.py` script of the app it is associated with. Let's start by creating a todo lists app by executing the following command:
```sh
python manage.py startapp todo_lists
```

We also need to add our todo lists app to the list of installed apps in `simple-todo/simple_todo/simple_todo/settings.py`:
```python
INSTALLED_APPS = [
    "layout",
    "accounts",
    "todo_lists",
    "allauth",
    "allauth.account",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Now we can create our data model classes by modifying `simple-todo/simple_todo/todo_lists/models.py` like this:
```python
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
```

Each data model class must extend the `models.Model` class and define one or more field objects. Foreign key fields can be used to establish relationships between data model classes. The cascading delete mode will ensure that when a data model instance is deleted, any data model instances which refer to it will be deleted as well. The related name will create an attribute on the referenced data model class which can be used to access all data model instances which refer to a referenced data model instance. Some types of fields such as character fields can have a maximum length set. You can also set a default value on a field. If you want a field to have a different name when rendered on a form you can set a verbose name on it. Data model classes can also contain a meta class with a `constraints` attribute that defines a list of constraints for the underlying table. It's also a good idea to create a `__str__` method which returns the string representation of a data model instance. This will be useful later when we register our data models with the Django admin site. Whenever we modify our data model classes we must also create and apply migrations for them to our database by executing the following commands:
```sh
python manage.py makemigrations
python manage.py migrate
```
