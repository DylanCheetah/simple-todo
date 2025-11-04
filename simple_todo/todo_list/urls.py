from django.urls import path

from . import views


urlpatterns = [
    path("", views.TodoListsView.as_view(), name="todo-lists"),
    path("todo-lists/<int:pk>/", views.TodoListView.as_view(), name="todo-list"),
    path("todo-lists/<int:pk>/edit/", views.TodoListUpdateView.as_view(), name="todo-list-edit"),
    path("todo-lists/<int:pk>/delete/", views.TodoListDeleteView.as_view(), name="todo-list-delete"),
    path("tasks/<int:pk>/edit/", views.TaskUpdateView.as_view(), name="task-edit"),
    path("tasks/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task-delete")
]
