# Lesson 4: Admin Site

Now that we have created our data model classes, we need to provide a way for site admins to manage them. Django provides an admin site for this purpose, but we will need to configure it so we can manage our new data models. First, we need to open `simple_todo/todo_list/admin.py` and modify it like this:
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
    list_display = ["name", "todo_list", "due_date", "completed"]
    ordering = ["name"]
    autocomplete_fields = ["todo_list"]
    search_fields = ["name", "todo_list__name", "todo_list__user__username"]
```

The first thing we do is import our data model classes. Afterwards, we can create one model admin class per data model class. Each model admin class must extend `admin.ModelAdmin`. The `list_display` attribute defines a list of fields to display when viewing a list of data model instances. The `ordering` attribute defines a list of fields to sort the data model instances by. The `autocomplete_fields` attribute defines a list of foreign key fields which should have a searchable select box on the admin for for creating and editing data model instances. The `search_fields` attribute defines a list of character or text fields to use when searching the list of data model instances. The `admin.register` decorator is applied to each model admin class to register the model admin classes. This decorator expects to receive the associated data model class as its first parameter. Afterwards, we need to create a superuser account:
```sh
python manage.py createsuperuser
```

You will be asked to provide a username, email address, and password. Afterwards, visit [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) in a web browser and you should see this page:
*screenshot*

Log in with the username and password you provided when creating the superuser account and you should see this page:
*screenshot*

Each app and its corresponding data models will be listed on this page. However, our todo list app is currently listed as "TODO_LIST" on this page. We can fix this by opening `simple_todo/todo_list/apps.py` and modifying it like this:
```python
from django.apps import AppConfig


class TodoListConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todo_list'
    verbose_name = "Todo List"
```

If you refresh the page, the todo list app should now be listed as "Todo List":
*screenshot*

Click on the Todo lists link and you should see this page:
*screenshot*

At the moment, we have no todo lists. Let's add some. Click the Add link beside the Todo lists link and you should see this page:
*screenshot*

Fill out the form and click the Save and add another button. Then add 2 more todo lists in a similar manner. Return to the Todo lists page, you should see something similar to this:
*screenshot*

If you click on any todo list, you will see a form you can use to edit or delete the todo list:
*screenshot*

Now that you have created some todo lists, try creating some tasks by clicking the Add link beside the Tasks link. Then visit the Tasks page to view the tasks you created. You can also try using the search box on the Tasks page to search tasks by their name and todo list. The Todo lists page has a search box as well which can be used to search by name or user. If you wish, you can also try creating additional users via the Add link beside the Users link and adding todo lists for those users as well.
