from django.urls import path

from .views import register


# Create URL mappings
urlpatterns = [
    path("register/", register, name="account-register")
]
