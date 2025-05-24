from django import forms


# Forms
# =====
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=64, widget=forms.TextInput({"class": "form-control"}))
    password = forms.CharField(min_length=8, max_length=128, widget=forms.TextInput({"class": "form-control", "type": "password"}))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, widget=forms.TextInput({"class": "form-control"}))
    password = forms.CharField(min_length=8, max_length=128, widget=forms.TextInput({"class": "form-control", "type": "password"}))
