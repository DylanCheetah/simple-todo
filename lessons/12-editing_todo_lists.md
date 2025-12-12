# Lesson 12: Editing Todo Lists

In order to edit a todo list we will provide a form when the edit button at the top of the page is clicked. We already created this form in the previous lesson, but we will need to create a view to serve the form and process the submitted data. We will also need a view that will fetch the todo list info if we click the cancel button on the form. Let's start by modifying `simple-todo/simple_todo/todo_lists/views.py` like this:
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
from .models import TodoList


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
```

The `TodoListUpdateView` class extends `UpdateView`. It works similar to a create view, but it is used to edit an existing data model instance. The `context_object_name` attribute is used to set the name of the template context variable which will contain the data model instance being edited. The `get_queryset` method determines which todo lists can be modified by the current user. Since we will just be editing an existing todo list this time, we will not reload the whole page. Instead we will replace the form with the new todo list info. Therefore, we will return the value returned by the base `form_valid` method. Since the success URL needs to be used to fetch the new todo list data, we will need to generate it dynamically by overriding the `get_success_url` method. This will allow us to the use the `pk` URL parameter in the `reverse` function. The `TodoListInfoView` class extends `DetailView`. The `template_name` attribute determines which template to render. The `context_object_name` attribute is used to set the name of the template context variable which will contain the data model instance being edited. The `get_queryset` method determines which todo lists can be accessed by the current user. We also modified our todo list view so that it dispatches HTTP POST requests to our new todo list update view. Next we need to open `simple-todo/simple_todo/todo_lists/urls.py` and modify it like this:
```python
from django.urls import path

from . import views


urlpatterns = [
    path("", views.TodoListsView.as_view(), name="todo-lists"),
    path("todo-lists/<int:pk>/", views.TodoListView.as_view(), name="todo-list"),
    path("todo-lists/<int:pk>/edit/", views.TodoListUpdateView.as_view(), name="todo-list-edit"),
    path("todo-lists/<int:pk>/info/", views.TodoListInfoView.as_view(), name="todo-list-info")
]
```

Now we need to modify `simple-todo/simple_todo/todo_lists/templates/todo_lists/todo_list_info.html` like this:
```html
<div id="todo_list-info" class="row justify-content-center">
    <h1 class="col-8">
        {{ todo_list.name }}
        <button class="btn btn-warning"
            hx-get="{% url 'todo-list-edit' todo_list.pk %}"
            hx-target="#todo_list-info"
            hx-swap="outerHTML">
            <div class="spinner-border spinner-border-sm htmx-indicator">
                <span class="visually-hidden">Loading...</span>
            </div>
            Edit
        </button>
    </h1>
</div>
```

We also need to modify `simple-todo/simple_todo/todo_lists/templates/todo_lists/todo_list_update_form.html` like this:
```html
<div id="todo_list-update-form" class="row justify-content-center">
    <form class="col-8"
          hx-post="{% url 'todo-list' todo_list.pk %}"
          hx-target="#todo_list-update-form"
          hx-swap="outerHTML">
          {% csrf_token %}
          {{ form }}
        <br/>
        <button class="m-1 btn btn-success">
            <div class="spinner-border spinner-border-sm htmx-indicator">
                <span class="visually-hidden">Loading...</span>
            </div>
            Save
        </button>
        <button class="m-1 btn btn-danger"
                type="button"
                hx-get="{% url 'todo-list-info' todo_list.pk %}"
                hx-target="#todo_list-update-form"
                hx-swap="outerHTML">
            <div class="spinner-border spinner-border-sm htmx-indicator">
                <span class="visually-hidden">Loading...</span>
            </div>
            Cancel
        </button>
    </form>
</div>
```

If we click the edit button beside the name on a todo list detail page, we should see this form appear now:
![todo list update form](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/15-todo_list_update_form.png?raw=true)

Clicking the save button will save any changes made and clicking the cancel button will discard any changes.
