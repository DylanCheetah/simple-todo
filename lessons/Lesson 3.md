# Lesson 3: Models

Now that we have our basic project structure setup, we can begin developing our todo list. Django projects are divided into separate apps. Therefore we will need to start by creating a new app within our Django project:
01. click Terminal > New Terminal
02. activate your virtual environment
03. execute `cd simple_todo`
04. execute `python manage.py startapp todo_list`

Note: Django app names can only contain alphanumeric characters and underscores.

Afterwards, your project structure should look like this:
```
simple-todo/
    simple_todo/
        simple_todo/
            __init__.py
            asgi.py
            settings.py
            urls.py
            wsgi.py
        todo_list/
            migrations/
            __init__.py
            admin.py
            apps.py
            models.py
            tests.py
            views.py
        manage.py
    venv/
    requirements.txt
```

Whenever we create a new Django app, we also need to open `simple_todo/simple_todo/settings.py` and add the name of the new app to the list of installed apps like this:
```python
INSTALLED_APPS = [
    "todo_list",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Now we can start defining the data model classes used by our todo list app. A Django data model class is used to manage a table of data in the database for our Django project. Open `simple_todo/todo_list/models.py` and modify it like this:
```python
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
```

We need 2 data model classes for our todo list app. The `TodoList` class has 2 fields and will represent a todo list. `user` will be a foreign key field which references the built-in `User` class and `name` will be the name of a todo list. By associating each todo list with a user, we can support multiple users. This is known as a multi-tenant web application. We set the delete mode of the `user` field to cascade so that all todo lists associated with a user will be deleted if a user is deleted. And we set the related name to "todo_lists" so we can easily get all the todo lists associated with a user via a `todo_lists` backreference attribute which will automatically be added to the `User` class. The `name` field will have a maximum length of 64 and be unique to prevent duplicate todo list names. The `__str__` method returns the string representation of data model instances. This will be useful when we register the data model class with the admin site.

The `Task` class has 4 fields and will represent a task on a todo list. `todo_list` will be a foreign key field which references the `TodoList` class, `name` will be the name of a task, `due_date` will be the due date of a task, and `completed` will indicate if a task has been completed. We set the delete mode of the `todo_list` field to cascade so that all tasks associated with a todo list will be deleted if a todo list is deleted. And we set the related name to "tasks" so we can easily get all the tasks associated with a todo list via a `tasks` attribute which will automatically be added to the `TodoList` class. The `name` field will have a maximum length of 64 and be unique to prevent duplicate task names. The `completed` field has a default value of False so we won't need to set it when we create a new task.

Whenever we modify our data model classes we will also need to make and apply migrations to the database for our Django project:
01. execute `python manage.py makemigrations`
02. execute `python manage.py migrate`

If all goes well, you should see a long list of migrations applied to the database. Some of them are for built-in Django apps such as admin, auth, contenttypes, and sessions. One of them is for our todo list app.
