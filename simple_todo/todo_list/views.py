from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .forms import TodoListForm
from .models import TodoList
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

    def form_valid(self, form):
        # Associate the new todo list with the current user
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class TodoListView(LoginRequiredMixin, View):
    login_url = reverse_lazy("user-login")
    
    def get(self, request, *args, **kwargs):
        # Dispatch HTTP GET requests to the list view
        view = TodoListListView.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # Dispatch HTTP POST requests to the create view
        view = TodoListCreateView.as_view()
        return view(request, *args, **kwargs)
