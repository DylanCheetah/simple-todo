from django.urls import path

from . import views


urlpatterns = [
    path("", views.TodoListsView.as_view(), name="todo-lists"),
    path("todo_lists/<int:pk>/", views.TodoListView.as_view(), name="todo-list"),
    path("todo_lists/<int:pk>/edit/", views.TodoListUpdateView.as_view(), name="todo-list-edit"),
    path("todo_lists/<int:pk>/info/", views.TodoListInfoView.as_view(), name="todo-list-info"),
    path("todo_lists/<int:pk>/create_task/", views.TaskCreateView.as_view(), name="todo-list-create-task")
]
