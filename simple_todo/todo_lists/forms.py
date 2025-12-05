from django import forms

from .models import TodoList


# Form Classes
# ============
class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ["name"]
        widgets = {
            "name": forms.TextInput({"class": "form-control"})
        }
