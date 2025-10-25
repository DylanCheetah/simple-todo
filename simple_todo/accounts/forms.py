from django import forms
from django.contrib.auth import forms as auth_forms


# Classes
# =======
class UserCreationForm(auth_forms.BaseUserCreationForm):
    class Meta(auth_forms.BaseUserCreationForm.Meta):
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"})
        }

    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Apply Bootstrap styling to password fields
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


class UserAuthenticationForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Apply Bootstrap styling to username and password fields
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["password"].widget.attrs.update({"class": "form-control"})
