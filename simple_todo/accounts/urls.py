from django.urls import path

from . import views


urlpatterns = [
    path("register/", views.UserCreateView.as_view(), name="user-create")
]
