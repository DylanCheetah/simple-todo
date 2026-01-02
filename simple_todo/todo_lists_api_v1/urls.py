from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from .views import TaskViewSet, TodoListViewSet


# Configure router
router = DefaultRouter()
router.register("todo-lists", TodoListViewSet, "todo_list")
router.register("tasks", TaskViewSet, "task")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls")),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh")
]
