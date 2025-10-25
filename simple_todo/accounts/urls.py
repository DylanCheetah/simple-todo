from django.urls import path

from . import views


urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="user-login"),
    path("logout/", views.UserLogoutView.as_view(), name="user-logout"),
    path("register/", views.UserCreateView.as_view(), name="user-create")
]
