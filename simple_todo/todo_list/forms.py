from django import forms

from .models import TodoList


# Classes
# =======
class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"})
        }
