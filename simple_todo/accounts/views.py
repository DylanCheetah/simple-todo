from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import UserCreationForm
from layout.views import LayoutMixin


# Classes
# =======
class UserCreateView(LayoutMixin, CreateView):
    template_name = "accounts/register.html"
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("user-login")
