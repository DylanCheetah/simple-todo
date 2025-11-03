# Lesson 10: Editing and Deleting Todo Lists

Now that we can view our todo lists and create new todo lists, we need to add a way to edit or delete a todo list. Let's start by creating a page for editing todo lists. Create `simple_todo/todo_list/templates/todo_list/todo_list_edit.html` with the following content:
```html
{% extends 'layout/layout.html' %}

{% block title %}Edit Todo {% endblock %}

{% block content %}
    <div class="row justify-content-center">
        <h1 class="col-8">Edit Todo List</h1>
    </div>
    <br/>
    <div class="row justify-content-center">
        <form class="col-8 card bg-light" method="POST">
            {% csrf_token %}
            <div class="card-body">
                {{ form }}
                <br/>
                <input class="btn btn-primary" type="submit" value="Save"/>
            </div>
        </form>
    </div>
{% endblock %}
```

Next we need to create a view which extends `UpdateView` and `LoginRequiredMixin`:
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView

from .forms import TaskForm, TodoListForm
from .models import Task, TodoList


# View Classes
# ============
class TodoListListView(ListView):
    template_name = "todo_list/todo_lists.html"
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.todo_lists.order_by("name")
    
    def get_context_data(self, **kwargs):
        # Add the todo list form to the context
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = TodoListForm()
        return ctx
    

class TodoListCreateView(CreateView):
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
    

class TodoListDetailView(SingleObjectMixin, ListView):
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
    

class TaskCreateView(CreateView):
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
    

class TodoListUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "todo_list/todo_list_edit.html"
    model = TodoList
    form_class = TodoListForm

    def get_queryset(self):
        return self.request.user.todo_lists.all()
    
    def get_success_url(self):
        return reverse("todo-list", args=(self.kwargs["pk"],))
```

The `template_name` attribute determines the template to use, the `model` attribute determines the data model class to use, and the `form_class` attribute determines the form class to use. We use `get_queryset` to prevent users from editing todo lists which aren't associated with them. And we define a `get_success_url` method which returns the URL of the todo list we are editing. Next we need to map our update view to a URL:
```python
from django.urls import path

from . import views


urlpatterns = [
    path("", views.TodoListsView.as_view(), name="todo-lists"),
    path("todo-lists/<int:pk>/", views.TodoListView.as_view(), name="todo-list"),
    path("todo-lists/<int:pk>/edit/", views.TodoListUpdateView.as_view(), name="todo-list-edit")
]
```

We also need to modify `simple_todo/todo_list/templates/todo_list/todo_list.html` like this:
```html
{% extends 'layout/layout.html' %}

{% block title %}Todo List{% endblock %}

{% block content %}
    <div class="row justify-content-center">
        <h1 class="col-7">{{ object.name }}</h1>
        <a class="col-1 m-2 btn btn-primary" href="{% url 'todo-list-edit' todo_list.pk %}">Edit</a>
    </div>
    <br/>
    <div class="row justify-content-center">
        <form class="col-8 card bg-light" method="POST">
            {% csrf_token %}
            <div class="card-body">
                <h3 class="card-title">New Task</h3>
                {{ form }}
                <br/>
                <input class="btn btn-primary" type="submit" value="Create Task"/>
            </div>
        </form>
    </div>
    <br/>
    <div class="row justify-content-center">
        <div class="col-8 card bg-light">
            <div class="card-body">
                <h3 class="card-title">Tasks</h3>
                {% for task in page_obj %}
                    <div class="row">
                        <div class="col m-1 card bg-light">
                            <div class="row card-body">
                                <a class="col-8 nav-link" href="">{{ task.name }}</a>
                                <div class="col-2">{{ task.due_date }}</div>
                                <a class="col-2 btn btn-danger" href="">Delete</a>
                            </div>
                        </div>
                    </div>
                {% empty %}
                    <div class="row">
                        <div class="col">No Data</div>
                    </div>
                {% endfor %}
                <br/>
                <div class="row justify-content-center">
                    {% if page_obj.has_previous %}
                        <a class="col-2 btn btn-primary" href="?page={{ page_obj.previous_page_number }}">Previous</a>
                    {% else %}
                        <a class="col-2 btn btn-secondary pe-none">Previous</a>
                    {% endif %}
                    <div class="col-2 text-center">Page {{ page_obj.number }} of {{ paginator.num_pages }}</div>
                    {% if page_obj.has_next %}
                        <a class="col-2 btn btn-primary" href="?page={{ page_obj.next_page_number }}">Next</a>
                    {% else %}
                        <a class="col-2 btn btn-secondary pe-none">Next</a>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
{% endblock %}
```

If you click the Edit button on any todo list details page now, you should see this page:
![todo list edit page](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/14-todo_list_edit.png?raw=true)

Now we can add a way to delete todo lists. First we need to create a class which extends `DeleteView` and
`LoginRequired`:
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import TaskForm, TodoListForm
from .models import Task, TodoList


# View Classes
# ============
class TodoListListView(ListView):
    template_name = "todo_list/todo_lists.html"
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.todo_lists.order_by("name")
    
    def get_context_data(self, **kwargs):
        # Add the todo list form to the context
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = TodoListForm()
        return ctx
    

class TodoListCreateView(CreateView):
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
    

class TodoListDetailView(SingleObjectMixin, ListView):
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
    

class TaskCreateView(CreateView):
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
    

class TodoListUpdateView(LoginRequiredMixin, UpdateView):
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
```

The `model` attribute determines the data model class to use and the `success_url` attribute determines the URL to redirect to on success. The `get_queryset` method is used to prevent users from deleting todo lists which aren't associated with them. Next we need to map the delete view to a URL:
```python
from django.urls import path

from . import views


urlpatterns = [
    path("", views.TodoListsView.as_view(), name="todo-lists"),
    path("todo-lists/<int:pk>/", views.TodoListView.as_view(), name="todo-list"),
    path("todo-lists/<int:pk>/edit/", views.TodoListUpdateView.as_view(), name="todo-list-edit"),
    path("todo-lists/<int:pk>/delete/", views.TodoListDeleteView.as_view(), name="todo-list-delete")
]
```

We also need to modify `simple_todo/todo_list/templates/todo_list/todo_lists.html` like this:
```html
{% extends 'layout/layout.html' %}

{% block title %}Todo Lists{% endblock %}

{% block content %}
    <div class="row justify-content-center">
        <h1 class="col-8">Todo Lists</h1>
    </div>
    <br/>
    <div class="row justify-content-center">
        <form class="col-8 card bg-light" method="POST">
            {% csrf_token %}
            <div class="card-body">
                <h3 class="card-title">New Todo List</h3>
                {{ form }}
                <br/>
                <input class="btn btn-primary" type="submit" value="Create Todo List"/>
            </div>
        </form>
    </div>
    <br/>
    <div class="row justify-content-center">
        <div class="col-8 card bg-light">
            <div class="card-body">
                <h3 class="card-title">Your Todo Lists</h3>
                {% for todo_list in page_obj %}
                    <div class="row">
                        <div class="col m-1 card bg-light">
                            <div class="row card-body">
                                <a class="col-10 nav-link" href="{% url 'todo-list' todo_list.pk %}">{{ todo_list.name }}</a>
                                <form class="col-2" method="POST" action="{% url 'todo-list-delete' todo_list.pk %}">
                                    {% csrf_token %}
                                    <div class="row">
                                        <input class="col btn btn-danger" type="submit" value="Delete"/>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                {% empty %}
                    <div class="row">
                        <div class="col">No Data</div>
                    </div>
                {% endfor %}
                <br/>
                <div class="row justify-content-center">
                    {% if page_obj.has_previous %}
                        <a class="col-2 btn btn-primary" href="?page={{ page_obj.previous_page_number }}">Previous</a>
                    {% else %}
                        <a class="col-2 btn btn-secondary pe-none">Previous</a>
                    {% endif %}
                    <div class="col-2 text-center">Page {{ page_obj.number }} of {{ paginator.num_pages }}</div>
                    {% if page_obj.has_next %}
                        <a class="col-2 btn btn-primary" href="?page={{ page_obj.next_page_number }}">Next</a>
                    {% else %}
                        <a class="col-2 btn btn-secondary pe-none">Next</a>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
{% endblock %}
```

Now we should be able to delete todo lists by clicking the Delete button beside them on the homepage. Notice that we have changed the Delete button from a link to a submit button inside a form. This is because HTTP GET requests cannot be used to modify data. If we were to visit our delete view with an HTTP GET request, we would get an error message about a missing delete confirmation template. It is possible to have a delete confirmation page for a delete view, but in this case we won't be using one.
