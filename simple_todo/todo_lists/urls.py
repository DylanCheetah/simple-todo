from django.urls import path

from . import views


urlpatterns = [
    path("", views.TodoListsView.as_view(), name="todo-lists"),
    path("todo_lists/<int:pk>/", views.TodoListView.as_view(), name="todo-list")
]
