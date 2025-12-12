# Lesson 13: Creating Tasks

The next feature we need to implement is the ability to create new tasks on a todo list. We already created the form we will need, but we still need to create the view which will handle creating new tasks and map it to a URL. Open `simple-todo/simple_todo/todo_lists/views.py` and modify it like this:
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView, 
    DeleteView, 
    DetailView, 
    ListView, 
    UpdateView, 
    View
)
from django.views.generic.detail import SingleObjectMixin
from django_htmx.http import HttpResponseClientRedirect

from .forms import TaskForm, TodoListForm
from .models import Task, TodoList


# View Classes
# ============
class TodoListsFullView(ListView):
    template_name = "todo_lists/todo_lists_full.html"
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.todo_lists.order_by("name")
    
    def get_context_data(self, **kwargs):
        # Add the todo list form to the template context
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = TodoListForm()
        return ctx
    

class TodoListsPartialView(ListView):
    template_name = "todo_lists/todo_lists_partial.html"
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.todo_lists.order_by("name")
    

class TodoListCreateView(CreateView):
    template_name = "todo_lists/todo_list_create_form.html"
    model = TodoList
    form_class = TodoListForm
    success_url = reverse_lazy("todo-lists")

    def form_valid(self, form):
        # Associate the new todo list with the current user and try to save the
        # new todo list
        try:
            form.instance.user = self.request.user
            super().form_valid(form)
            return HttpResponseClientRedirect(self.get_success_url())
        
        except IntegrityError:
            form.add_error("name", "Duplicate todo list name.")
            return self.form_invalid(form)
    

class TodoListsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Render partial content?
        if request.htmx:
            view = TodoListsPartialView.as_view()

        else:
            view = TodoListsFullView.as_view()

        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # Dispatch to the todo list create view
        view = TodoListCreateView.as_view()
        return view(request, *args, **kwargs)
    

class TodoListFullView(SingleObjectMixin, ListView):
    template_name = "todo_lists/todo_list_full.html"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        # Store the referenced object and return the value returned by the
        # base method
        self.object = self.get_object(
            queryset=self.request.user.todo_lists.all()
        )
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        return self.object.tasks.order_by("name")
    
    def get_context_data(self, **kwargs):
        # Add the todo list and task form to the template context
        ctx = super().get_context_data(**kwargs)
        ctx["todo_list"] = self.object
        ctx["form"] = TaskForm()
        return ctx
    

class TasksPartialView(SingleObjectMixin, ListView):
    template_name = "todo_lists/tasks_partial.html"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        # Store the referenced object and return the value returned by the
        # base method
        self.object = self.get_object(
            queryset=self.request.user.todo_lists.all()
        )
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.tasks.order_by("name")
    
    def get_context_data(self, **kwargs):
        # Add the todo list to the template context
        ctx = super().get_context_data(**kwargs)
        ctx["todo_list"] = self.object
        return ctx
    

class TodoListUpdateView(UpdateView):
    template_name = "todo_lists/todo_list_update_form.html"
    context_object_name = "todo_list"
    model = TodoList
    form_class = TodoListForm

    def get_queryset(self):
        return self.request.user.todo_lists.all()

    def get_success_url(self):
        return reverse("todo-list-info", args=(self.kwargs["pk"],))

    def form_valid(self, form):
        # Try to update the todo list
        try:
            return super().form_valid(form)
        
        except IntegrityError:
            form.add_error("name", "Duplicate todo list name.")
            return self.form_invalid(form)
        

class TodoListInfoView(DetailView):
    template_name = "todo_lists/todo_list_info.html"
    context_object_name = "todo_list"
    
    def get_queryset(self):
        return self.request.user.todo_lists.all()


class TodoListDeleteView(DeleteView):
    success_url = reverse_lazy("todo-lists")

    def get_queryset(self):
        return self.request.user.todo_lists.all()
    
    def delete(self, request, *args, **kwargs):
        # Delete the todo list and redirect to the homepage
        super().delete(request, *args, **kwargs)
        return HttpResponseClientRedirect(self.get_success_url())


class TodoListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Render partial content?
        if request.htmx:
            view = TasksPartialView.as_view()

        else:
            view = TodoListFullView.as_view()

        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # Dispatch to the todo list update view
        view = TodoListUpdateView.as_view()
        return view(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # Dispatch to the todo list delete view
        view = TodoListDeleteView.as_view()
        return view(request, *args, **kwargs)
    

class TaskCreateView(CreateView):
    template_name = "todo_lists/task_create_form.html"
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse("todo-list", args=(self.kwargs["pk"],))
    
    def get_context_data(self, **kwargs):
        # Add the referenced todo list to the template context
        ctx = super().get_context_data(**kwargs)
        ctx["todo_list"] = self.get_object(
            queryset=self.request.user.todo_lists.all()
        )
        return ctx
    
    def form_valid(self, form):
        # Try to associate the new task with the referenced todo list and
        # save it
        try:
            form.instance.todo_list = self.get_object(
                queryset=self.request.user.todo_lists.all()
            )
            super().form_valid(form)
            return HttpResponseClientRedirect(self.get_success_url())
        
        except IntegrityError:
            form.add_error("name", "Duplicate task name.")
            return self.form_invalid(form)
```

In our new `TaskCreateView` the success URL needs to be dynamically generated so it refers to the todo list which we are adding a task to. The `get_success_url` method can be overridden for this purpose. We override the `get_context_data` method to add the referenced todo list to the template context. We can pass the primary key of the todo list via the `pk` URL parameter. The new task also needs to be associated with the todo list we are adding it to. This will allow us to get the correct todo list by calling the `get_object` method of our new view with a queryset containing the todo lists which belong to the current user. The rest of our new view is similar to our `TodoListCreateView`. Now we need to associate our new view with a URL. Open `simple-todo/simple_todo/todo_lists/urls.py` and modify it like this:
```python
from django.urls import path

from . import views


urlpatterns = [
    path("", views.TodoListsView.as_view(), name="todo-lists"),
    path("todo-lists/<int:pk>/", views.TodoListView.as_view(), name="todo-list"),
    path("todo-lists/<int:pk>/edit/", views.TodoListUpdateView.as_view(), name="todo-list-edit"),
    path("todo-lists/<int:pk>/info/", views.TodoListInfoView.as_view(), name="todo-list-info"),
    path("todo-lists/<int:pk>/create-task/", views.TaskCreateView.as_view(), name="todo-list-create-task")
]
```

We also need to modify `simple-todo/simple_todo/todo_lists/templates/todo_lists/task_create_form.html` like this:
```html
<form hx-post="{% url 'todo-list-create-task' todo_list.pk %}" hx-swap="outerHTML">
    {% csrf_token %}
    {{ form }}
    <br/>
    <button class="btn btn-primary">
        <div class="spinner-border spinner-border-sm htmx-indicator">
            <span class="visually-hidden">Loading...</span>
        </div>
        Create
    </button>
</form>
```

Now we should be able to use the new task form on the details page for a todo list to add a new task to the todo list.
