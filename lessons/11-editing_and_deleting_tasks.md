# Lesson 11: Editing and Deleting Tasks

Now that we are able to edit and delete todo lists, we also need a way to edit and delete tasks on them. Let's start by adding the ability to edit a task. First we need to create `simple_todo/todo_list/templates/todo_list/task_edit.html` with the following content:
```html
{% extends 'layout/layout.html' %}

{% block title %}Edit Task{% endblock %}

{% block content %}
    <div class="row justify-content-center">
        <h1 class="col-8">Edit Task</h1>
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

Next we need to open `simple_todo/todo_list/views.py` and modify it like this:
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
    

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "todo_list/task_edit.html"
    model = Task
    form_class = TaskForm

    def get_queryset(self):
        return Task.objects.filter(todo_list__user=self.request.user)
    
    def get_success_url(self):
        return reverse("todo-list", args=(self.object.todo_list.pk,))
```

This time we will need to use a more complex query in order to get the tasks we are able to modify. We filter the tasks based on if their parent todo list is owned by the current user. Also, we will redirect to the page for the todo list containing the task. Next we need to map our new view to a URL:
```python
from django.urls import path

from . import views


urlpatterns = [
    path("", views.TodoListsView.as_view(), name="todo-lists"),
    path("todo-lists/<int:pk>/", views.TodoListView.as_view(), name="todo-list"),
    path("todo-lists/<int:pk>/edit/", views.TodoListUpdateView.as_view(), name="todo-list-edit"),
    path("todo-lists/<int:pk>/delete/", views.TodoListDeleteView.as_view(), name="todo-list-delete"),
    path("tasks/<int:pk>/edit/", views.TaskUpdateView.as_view(), name="task-edit")
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
                                <a class="col-8 nav-link" href="{% url 'task-edit' task.pk %}">{{ task.name }}</a>
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

Now if you click one of the tasks on a todo list, you should see this page:
![task edit page](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/15-task_edit.png?raw=true)

Next, let's add the ability to delete a task. Modify `simple_todo/todo_list/views.py` like this:
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
    

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "todo_list/task_edit.html"
    model = Task
    form_class = TaskForm

    def get_queryset(self):
        return Task.objects.filter(todo_list__user=self.request.user)
    
    def get_success_url(self):
        return reverse("todo-list", args=(self.object.todo_list.pk,))
    

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task

    def get_queryset(self):
        return Task.objects.filter(todo_list__user=self.request.user)
    
    def get_success_url(self):
        return reverse("todo-list", args=(self.object.todo_list.pk,))
```

Notice that this time we need to generate the success URL dynamically. We also need to map our new view to a URL:
```python
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
```

And we also need to modify `simple_todo/todo_list/templates/todo_list/todo_list.html` like this:
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
                                <a class="col-8 nav-link" href="{% url 'task-edit' task.pk %}">{{ task.name }}</a>
                                <div class="col-2">{{ task.due_date }}</div>
                                <form class="col-2" method="POST" action="{% url 'task-delete' task.pk %}">
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

Now you should be able to delete a task by clicking its Delete button.
