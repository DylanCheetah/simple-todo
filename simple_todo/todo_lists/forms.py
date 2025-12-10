from django import forms

from .models import Task, TodoList


# Form Classes
# ============
class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ["name"]
        widgets = {
            "name": forms.TextInput({"class": "form-control"})
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "due_date"]
        widgets = {
            "name": forms.TextInput({"class": "form-control"}),
            "due_date": forms.DateTimeInput({"class": "form-control", "type": "datetime-local"})
        }
