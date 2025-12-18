from django.urls import path

from . import views


urlpatterns = [
    path("", views.TodoListsView.as_view(), name="todo-lists"),
    path("todo-lists/<int:pk>/", views.TodoListView.as_view(), name="todo-list"),
    path("todo-lists/<int:pk>/edit/", views.TodoListUpdateView.as_view(), name="todo-list-edit"),
    path("todo-lists/<int:pk>/info/", views.TodoListInfoView.as_view(), name="todo-list-info"),
    path("todo-lists/<int:pk>/create-task/", views.TaskCreateView.as_view(), name="todo-list-create-task"),
    path("tasks/<int:pk>/", views.TaskDeleteView.as_view(), name="task"),
    path("tasks/<int:pk>/edit/", views.TaskUpdateView.as_view(), name="task-edit"),
    path("tasks/<int:pk>/info/", views.TaskInfoView.as_view(), name="task-info")
]
