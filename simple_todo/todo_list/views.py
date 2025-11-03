from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import TaskForm, TodoListForm
from .models import Task, TodoList
from layout.views import LayoutMixin


# Classes
# =======
class TodoListListView(LayoutMixin, ListView):
    template_name = "todo_list/todo_lists.html"
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.todo_lists.order_by("name")
    
    def get_context_data(self, **kwargs):
        # Add the todo list form to the context
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = TodoListForm()
        return ctx
    

class TodoListCreateView(LayoutMixin, CreateView):
    model = TodoList
    form_class = TodoListForm
    success_url = reverse_lazy("todo-lists")

    def form_valid(self, form):
        # Associate the new todo list with the current user
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class TodoListsView(LoginRequiredMixin, View):
    login_url = reverse_lazy("user-login")
    
    def get(self, request, *args, **kwargs):
        # Dispatch HTTP GET requests to the list view
        view = TodoListListView.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # Dispatch HTTP POST requests to the create view
        view = TodoListCreateView.as_view()
        return view(request, *args, **kwargs)
    

class TodoListDetailView(LayoutMixin, SingleObjectMixin, ListView):
    template_name = "todo_list/todo_list.html"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        # Store the referenced object and return the value returned by the 
        # base method
        self.object = self.get_object(
            queryset=self.request.user.todo_lists.all())
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        return self.object.tasks.order_by("name")
    
    def get_context_data(self, **kwargs):
        # Add the todo list and task form to the context
        ctx = super().get_context_data(**kwargs)
        ctx["todo_list"] = self.object
        ctx["form"] = TaskForm()
        return ctx
    

class TaskCreateView(LayoutMixin, CreateView):
    model = Task
    form_class = TaskForm

    def form_valid(self, form):
        # Associate the new task with the referenced todo list
        form.instance.todo_list = self.get_object(
            queryset=self.request.user.todo_lists.all())
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("todo-list", args=(self.kwargs["pk"],))
    

class TodoListView(LoginRequiredMixin, View):
    login_url = reverse_lazy("user-login")

    def get(self, request, *args, **kwargs):
        # Dispatch HTTP GET requests to the todo list detail view
        view = TodoListDetailView.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # Dispatch HTTP POST requests to the task create view
        view = TaskCreateView.as_view()
        return view(request, *args, **kwargs)
    

class TodoListUpdateView(LoginRequiredMixin, LayoutMixin, UpdateView):
    template_name = "todo_list/todo_list_edit.html"
    model = TodoList
    form_class = TodoListForm

    def get_queryset(self):
        return self.request.user.todo_lists.all()
    
    def get_success_url(self):
        return reverse("todo-list", args=(self.kwargs["pk"],))
    

class TodoListDeleteView(LoginRequiredMixin, DeleteView):
    model = TodoList
    success_url = reverse_lazy("todo-lists")

    def get_queryset(self):
        return self.request.user.todo_lists.all()
