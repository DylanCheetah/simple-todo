# Lesson 11: Todo List Details

In order to view the details for each todo list, we will need to create a todo list details page. The todo list details page will display the name of a single todo list, provide a button to edit the todo list, provide a form to add a task to the todo list, and display the tasks on the todo list. Usually a `DetailView` would be used for this sort of page, but in this case we need pagination for the list of tasks on each todo list. So we will need to create a view which behaves like both a `DetailView` and a `ListView`. First let's create the templates we will need. Create `simple-todo/simple_todo/todo_lists/templates/todo_lists/todo_list_info.html` with the following content:
```html
<div id="todo_list-info" class="row justify-content-center">
    <h1 class="col-8">
        {{ todo_list.name }}
        <button class="btn btn-warning"
            hx-get=""
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

This template will simply display the name of a todo list as a heading and an edit button. Next we need to create `simple-todo/simple_todo/todo_lists/templates/todo_lists/todo_list_update_form.html` with the following content:
```html
<div id="todo_list-update-form" class="row justify-content-center">
    <form class="col-8"
          hx-put=""
          hx-target="#todo_list-update-form"
          hx-swap="outerHTML">
          {% csrf_token %}
          {{ form }}
        <br/>
        <button class="m-1 btn btn-success">
            <div class="spinner-border spinner-border-sm htmx-indicator">
                <span class="visually-hidden">Loading...</span>
                Save
            </div>
        </button>
        <button class="m-1 btn btn-danger"
                type="button"
                hx-get=""
                hx-target="#todo_list-update-form"
                hx-swap="outerHTML">
            <div class="spinner-border spinner-border-sm htmx-indicator">
                <span class="visually-hidden">Loading...</span>
                Cancel
            </div>
        </button>
    </form>
</div>
```

This form will be displayed after clicking the edit button beside the todo list name. We can use the same form class for our create and update forms, but we do need to create a form class for our task create form. Open `simple-todo/simple_todo/todo_lists/forms.py` and modify it like this:
```python
from django import forms

from .models import Task, TodoList


# Form Classes
# ============
class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ["name"]
        widgets = {
            "name": forms.TextInput({"class": "form-control"})
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "due_date"]
        widgets = {
            "name": forms.TextInput({"class": "form-control"}),
            "due_date": forms.DateTimeInput({"class": "form-control", "type": "datetime-local"})
        }
```

Next, create `simple-todo/simple_todo/todo_lists/templates/todo_lists/task_create_form.html` with the following content:
```html
<form hx-post="" hx-swap="outerHTML">
    {% csrf_token %}
    {% if task_create_err %}
        <div class="alert alert-danger">{{ task_create_err }}</div>
    {% endif %}
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

Now we need to create `simple-todo/simple_todo/todo_lists/templates/todo_lists/tasks_partial.html` with the following content:
```html
<div id="tasks-view">
    {% for task in page_obj %}
        <div class="row justify-content-center">
            <div class="col m-1 card bg-light">
                <div class="card-body row">
                    <div class="col-8 nav-link">{{ task.name }}</div>
                    <form class="col-2" 
                          hx-put=""
                          hx-target="#tasks-view"
                          hx-swap="outerHTML">
                          {% csrf_token %}
                        <button class="col-12 btn btn-warning">
                            <div class="spinner-border spinner-border-sm htmx-indicator">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            Edit
                        </button>
                    </form>
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

Next we need to create `simple-todo/simple_todo/todo_lists/templates/todo_lists/todo_list_full.html` with the following content:
```html
{% extends "layout/base.html" %}

{% block title %}Todo List Details{% endblock %}

{% block content %}
    {% include "todo_lists/todo_list_info.html" %}
    <div class="row justify-content-center">
        <div class="col-8 m-2 card bg-light">
            <div class="card-body">
                <h3 class="card-title">New Task</h3>
                {% include "todo_lists/task_create_form.html" %}
            </div>
        </div>
    </div>
    <div class="row justify-content-center">
        <div class="col-8 m-2 card bg-light">
            <div class="card-body">
                <h3 class="card-title">Tasks</h3>
                {% include "todo_lists/tasks_partial.html" %}
            </div>
        </div>
    </div>
{% endblock %}
```

Now we can create our todo list detail view. In order to make it behave like both a detail view and list view we will have it extend `SingleObjectMixin` and `ListView`. The `SingleObjectMixin` class defines a `get_object` method we can use to get the object we are trying to view based on the `pk` URL parameter and a given queryset object. We also need a view to display a page of tasks. We will dispatch requests to our new views with our existing `TodoListView` class. Open `simple-todo/simple_todo/todo_lists/views.py` and modify it like this:
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, View
from django.views.generic.detail import SingleObjectMixin
from django_htmx.http import HttpResponseClientRedirect

from .forms import TaskForm, TodoListForm


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
    

class TodoListCreateView(TemplateView):
    template_name = "todo_lists/todo_list_create_form.html"
    success_url = reverse_lazy("todo-lists")

    def post(self, request, *args, **kwargs):
        # Validate the todo list form
        form = TodoListForm(request.POST)

        if not form.is_valid():
            # Return the form to be corrected
            ctx = self.get_context_data()
            ctx["form"] = form
            return render(request, self.template_name, ctx)
        
        # Save the new todo list
        try:
            form.instance.user = request.user
            form.save()

        except IntegrityError:
            # Return the form to be corrected
            ctx = self.get_context_data()
            ctx["form"] = form
            ctx["todo_list_create_err"] = "Duplicate todo list name. Please change the name and try again."
            return render(request, self.template_name, ctx)

        return HttpResponseClientRedirect(self.success_url)
    

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
    

class TaskPartialView(SingleObjectMixin, ListView):
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
    

class TodoListDeleteView(View):
    success_url = reverse_lazy("todo-lists")

    def get_queryset(self):
        return self.request.user.todo_lists.all()

    def delete(self, request, *args, **kwargs):
        # Delete the requested todo list
        todo_list = get_object_or_404(self.get_queryset(), pk=kwargs["pk"])
        todo_list.delete()
        return HttpResponseClientRedirect(self.success_url)


class TodoListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Render partial content?
        if request.htmx:
            view = TaskPartialView.as_view()

        else:
            view = TodoListFullView.as_view()

        return view(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # Dispatch to the todo list delete view
        view = TodoListDeleteView.as_view()
        return view(request, *args, **kwargs)
```

Next we need to modify `simple-todo/simple_todo/todo_lists/templates/todo_lists_partial.html` like this:
```html
<div id="todo_lists-view">
    {% for todo_list in page_obj %}
        <div class="row">
            <div class="col m-1 card bg-light">
                <div class="card-body row">
                    <a class="col-10 nav-link" href="{% url 'todo-list' todo_list.pk %}">{{ todo_list.name }}</a>
                    <form class="col-2"
                          hx-delete="{% url 'todo-list' todo_list.pk %}"
                          hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
                        <button class="col-12 btn btn-danger">
                            <div class="spinner-border spinner-border-sm htmx-indicator">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            Delete
                        </button>
                    </form>
                </div>
            </div>
        </div>
    {% empty %}
        No Data
    {% endfor %}
    <br/>
    <div class="row justify-content-center">
        {% if page_obj.has_previous %}
            <button class="col-2 btn btn-primary"
                    hx-get="{% url 'todo-lists' %}?page={{ page_obj.previous_page_number }}"
                    hx-target="#todo_lists-view" 
                    hx-swap="outerHTML"
                    hx-push-url="true">
                    <div class="spinner-border spinner-border-sm htmx-indicator" role="status">
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
                    hx-get="{% url 'todo-lists' %}?page={{ page_obj.next_page_number }}"
                    hx-target="#todo_lists-view"
                    hx-swap="outerHTML"
                    hx-push-url="true">
                    <div class="spinner-border spinner-border-sm htmx-indicator" role="status">
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

If you click one of the todo lists on the homepage, you should see a page like this now:
*screenshot*
