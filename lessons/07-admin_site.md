# Lesson 07: Admin Site

Django provides an admin site which we can use to manage the data model instances for our website. But before we can use it to manage instances of a data model, we must first register each data model class with the admin site. To register your data models, create model admin classes in `simple-todo/simple_todo/todo_lists/admin.py` like this:
```python
from django.contrib import admin

from .models import Task, TodoList


# Model Admin Classes
# ===================
@admin.register(TodoList)
class TodoListAdmin(admin.ModelAdmin):
    list_display = ["name", "user"]
    ordering = ["name"]
    autocomplete_fields = ["user"]
    search_fields = ["name", "user__username"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "todo_list", "due_date", "is_completed"]
    ordering = ["name"]
    autocomplete_fields = ["todo_list"]
    search_fields = ["name", "todo_list__name", "todo_list__user__username"]
```

Each model admin class must extend `admin.ModelAdmin`. The `list_display` attribute determines which fields will be displayed in each data model list page, the `ordering` attribute determines which field the data model instances will be sorted by, the `autocomplete_fields` attribute can be used to provide a searchable list box for foreign key fields instead of the default dropdown box, and the `search_fields` attribute determines which fields are used when searching for data model instances. We can also set the name of the category displayed for our todo lists app by modifying `simple-todo/simple_todo/todo_lists/apps.py` like this:
```python
from django.apps import AppConfig


class TodoListsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todo_lists'
    verbose_name = "Todo Lists"
```

If you visit http://127.0.0.1:8000/admin/ in your web browser, you should see this page:
![admin login](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/05-admin_login.png?raw=true)

Enter the username and password you chose when you created the superuser account and you should see this page:
![admin site homepage](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/06-admin_site_homepage.png?raw=true)

There will be one category for each installed app which has registered data model classes. Each registered data model class will be listed within the category for the app it belongs to. Click the todo lists link and you should see this page:
![empty todo lists admin page](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/07-empty_todo_lists_admin_page.png?raw=true)

If you click the Add link beside the todo lists link, you should see this page:
![todo list create form](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/08-todo_list_create_form.png?raw=true)

Try adding a few todo lists and you should see something like this on the todo lists page:
![todo lists admin page](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/09-todo_lists_admin_page.png?raw=true)

Click the Add link beside the tasks link and you should see this page:
![task create form](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/10-task_create_form.png?raw=true)

Now add some tasks to each todo list and you should see something like this on the tasks page:
![tasks admin page](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/11-tasks_admin_page.png?raw=true)

The search box at the top of the todo lists and tasks pages can also be used to search the list of data model instances on each page. You can also click on a data model instance to edit or delete it. The checkboxes on each data model list page can be used to select multiple data model instances in order to perform an action on multiple instances at once.
