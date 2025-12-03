from allauth.account import forms


# Form Classes
# ============
class LoginForm(forms.LoginForm):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Add Bootstrap styling to the form fields
        self.fields["login"].widget.attrs.update({"class": "form-control"})
        self.fields["password"].widget.attrs.update({"class": "form-control"})
        self.fields["remember"].widget.attrs.update({"class": "form-check-input"})


class SignupForm(forms.SignupForm):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Add Bootstrap styling to the form fields
        self.fields["email"].widget.attrs.update({"class": "form-control"})
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


class AddEmailForm(forms.AddEmailForm):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Add Bootstrap styling to the form fields
        self.fields["email"].widget.attrs.update({"class": "form-control"})


class ChangePasswordForm(forms.ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Add Bootstrap styling to the form fields
        self.fields["oldpassword"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


class SetPasswordForm(forms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Add Bootstrap styling to the form fields
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


class ResetPasswordForm(forms.ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Add Bootstrap styling to the form fields
        self.fields["email"].widget.attrs.update({"class": "form-control"})


class ResetPasswordKeyForm(forms.ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Add Bootstrap styling to the form fields
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})
