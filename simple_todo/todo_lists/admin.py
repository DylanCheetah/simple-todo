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
