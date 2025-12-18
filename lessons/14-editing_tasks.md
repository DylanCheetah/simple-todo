# Lesson 14: Editing Tasks

In order to edit tasks on a todo list we will need a new form template and a new update view. We will also need a new detail view which serves the info for a single task on a todo list. Create `simple-todo/simple_todo/todo_lists/templates/todo_lists/task_update_form.html` with the following content:
```html
<form id="task-{{ task.pk }}"
      class="card-body row"
      hx-post="{% url 'task-edit' task.pk %}"
      hx-target="#task-{{ task.pk }}",
      hx-swap="outerHTML">
      {% csrf_token %}
      {{ form }}
    <button class="btn btn-success">
        <div class="spinner-border spinner-border-sm htmx-indicator">
            <span class="visually-hidden">Loading...</span>
        </div>
        Save
    </button>
    <button class="btn btn-danger"
            type="button"
            hx-get="{% url 'task-info' task.pk %}"
            hx-target="#task-{{ task.pk }}"
            hx-swap="outerHTML">
        <div class="spinner-border spinner-border-sm htmx-indicator">
            <span class="visually-hidden">Loading...</span>
        </div>
        Cancel
    </button>
</form>
```

Next we need to create `simple-todo/simple_todo/todo_lists/templates/todo_lists/task_info.html` with the following content:
```html
<div id="task-{{ task.pk }}" class="card-body row">
    <div class="col-8">
        <div class="row">
            <div class="col-12">{{ task.name }}</div>
        </div>
        <div class="row">
            <div class="col-12 text-secondary">{{ task.due_date }}</div>
        </div>
    </div>
    <div class="col-2">
        <button class="col-12 btn btn-warning"
                hx-get="{% url 'task-edit' task.pk %}"
                hx-target="#task-{{ task.pk }}"
                hx-swap="outerHTML">
            <div class="spinner-border spinner-border-sm htmx-indicator">
                <span class="visually-hidden">Loading...</span>
            </div>
            Edit
        </button>
    </div>
    <form class="col-2"
            hx-delete=""
            hx-target="#tasks-view"
            hx-swap="outerHTML"
            hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
        <button class="col-12 btn btn-danger">
            <div class="spinner-border spinner-border-sm htmx-indicator">
                <span class="visually-hidden">Loading...</span>
            </div>
            Delete
        </button>
    </form>
</div>
```

Since the template for the task info is identical to the code for each task in our partial tasks template, we can simply `simple-todo/simple_todo/todo_lists/templates/todo_lists/tasks_partial.html` like this:
```html
<div id="tasks-view">
    {% for task in page_obj %}
        <div class="row justify-content-center">
            <div class="col m-1 card bg-light">
                {% include "todo_lists/task_info.html" %}
            </div>
        </div>
    {% empty %}
        No Data
    {% endfor %}
    <br/>
    <div class="row justify-content-center">
        {% if page_obj.has_previous %}
            <button class="col-2 btn btn-primary"
                    hx-get="{% url 'todo-list' todo_list.pk %}?page={{ page_obj.previous_page_number }}"
                    hx-target="#tasks-view"
                    hx-swap="outerHTML"
                    hx-push-url="true">
                    <div class="spinner-border spinner-border-sm htmx-indicator">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    Previous
            </button>
        {% else %}
            <button class="col-2 btn btn-secondary pe-none">Previous</button>
        {% endif %}
        <div class="col-2 text-center">Page {{ page_obj.number }} of {{ paginator.num_pages }}</div>
        {% if page_obj.has_next %}
            <button class="col-2 btn btn-primary"
                    hx-get="{% url 'todo-list' todo_list.pk %}?page={{ page_obj.next_page_number }}"
                    hx-target="#tasks-view"
                    hx-swap="outerHTML"
                    hx-push-url="true">
                <div class="spinner-border spinner-border-sm htmx-indicator">
                    <span class="visually-hidden">Loading...</span>
                </div>
                Next
            </button>
        {% else %}
            <button class="col-2 btn btn-secondary pe-none">Next</button>
        {% endif %}
    </div>
</div>
```

Now we can create our new views in `simple-todo/simple_todo/todo_lists/views.py` like this:
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
        

class TaskUpdateView(UpdateView):
    template_name = "todo_lists/task_update_form.html"
    context_object_name = "task"
    model = Task
    form_class = TaskForm
    
    def get_success_url(self):
        return reverse("task-info", args=(self.kwargs["pk"],))
    
    def get_queryset(self):
        return Task.objects.filter(todo_list__user=self.request.user)
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        
        except IntegrityError:
            form.add_error("name", "Duplicate task name.")
            return self.form_invalid(form)


class TaskInfoView(DetailView):
    template_name = "todo_lists/task_info.html"
    context_object_name = "task"

    def get_queryset(self):
        return Task.objects.filter(todo_list__user=self.request.user)
```

Next we need to map our new views to URLs. Open `simple-todo/simple_todo/todo_lists/urls.py` and modify it like this:
```python
from django.urls import path

from . import views


urlpatterns = [
    path("", views.TodoListsView.as_view(), name="todo-lists"),
    path("todo-lists/<int:pk>/", views.TodoListView.as_view(), name="todo-list"),
    path("todo-lists/<int:pk>/edit/", views.TodoListUpdateView.as_view(), name="todo-list-edit"),
    path("todo-lists/<int:pk>/info/", views.TodoListInfoView.as_view(), name="todo-list-info"),
    path("todo-lists/<int:pk>/create-task/", views.TaskCreateView.as_view(), name="todo-list-create-task"),
    path("tasks/<int:pk>/edit/", views.TaskUpdateView.as_view(), name="task-edit"),
    path("tasks/<int:pk>/info/", views.TaskInfoView.as_view(), name="task-info")
]
```

Now if you click the edit button beside any task on a todo list you will see a form like this:
![task update form](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/16-task_update_form.png?raw=true)

Clicking the save button will save any changes made to the task and clicking the cancel button will discard any changes. Afterwards, the info for the task will be displayed again.
