from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import UserAuthenticationForm, UserCreationForm


# View Classes
# ============
class UserCreateView(CreateView):
    template_name = "accounts/register.html"
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("user-login")


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = UserAuthenticationForm


class UserLogoutView(LogoutView):
    pass
