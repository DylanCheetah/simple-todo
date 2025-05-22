# Lesson 06: Register Data Models with Admin Site

To manage our data models more easily, we need to register them with the admin site. This will allow us to manage them via the admin site. Open `simple_todo/api/admin.py` and modify it like this:
```python
from django.contrib import admin

from .models import Task, TodoList


# Model Admin Classes
# ===================
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "todo_list", "due_date"]
    search_fields = ["name"]


class TodoListAdmin(admin.ModelAdmin):
    list_display = ["name", "owner__username"]
    search_fields = ["name", "owner__username"]


# Register data models
admin.site.register(Task, TaskAdmin)
admin.site.register(TodoList, TodoListAdmin)
```

At this point you should be able to manage your data models via admin site. Execute `python manage.py runserver` and visit [http://localhost:8000/admin/](http://localhost:8000/admin/) in a web browser. After you log in you should see your todo list and task data models. Try creating a few todo lists via the admin site and add some tasks to them.
