from django.urls import path

from .views import login_view, register


# Create URL mappings
urlpatterns = [
    path("register/", register, name="account-register"),
    path("login/", login_view, name="account-login")
]
