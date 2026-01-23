from django.urls import include, path

from . import views


urlpatterns = [
    path("", include("allauth.urls")),
    path("delete/", views.AccountDeleteView.as_view(), name="account-delete")
]
