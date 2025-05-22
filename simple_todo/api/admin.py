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
