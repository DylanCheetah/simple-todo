from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, TodoListViewSet


# Create router
router = DefaultRouter()
router.register("todo-lists", TodoListViewSet, "todolist")
router.register("tasks", TaskViewSet, "task")

# Define routes
urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls"))
]
