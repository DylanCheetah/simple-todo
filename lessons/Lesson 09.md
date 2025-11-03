# Lesson 09: Todo List Details

Now that we have a way to view our todo lists and create new todo lists, we also need a todo list details
page. Our todo list details page should display the name of the todo list, a form for adding tasks, and a list of tasks. Create `simple_todo/todo_list/templates/todo_list/todo_list.html` with the following content:
```html
{% extends 'layout/layout.html' %}

{% block title %}Todo List{% endblock %}

{% block content %}
    <div class="row justify-content-center">
        <h1 class="col-7">{{ object.name }}</h1>
        <a class="col-1 m-2 btn btn-primary" href="">Edit</a>
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

Next we need to create a new form for creating tasks. Open `simple_todo/todo_list/forms.py` and modify it like this:
```python
from django import forms

from .models import Task, TodoList


# Classes
# =======
class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"})
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "due_date"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "due_date": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"})
        }
```

We also need to create the view for our todo list details page. Since this view should display the details of a todo list and provide a form for creating tasks, we will need to create 2 views similar to what we did for our homepage. But in this case, we need to know which todo list we need to view. One way to do this would be to create a view based on `DetailView`. However, we also need a paginated list to display the tasks on the todo list. We cannot create a view which extends both `ListView` and `DetailView` because they would conflict. However, we can do this by creating a view which extends `ListView` and `SingleObjectMixin`. Open `simple_todo/todo_list/views.py` and modify it like this:
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView

from .forms import TaskForm, TodoListForm
from .models import TodoList


# Classes
# =======
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
```

We include the same attributes needed by `ListView`. However, we need to override the `get` method so we can fetch the todo list we wish to view by calling the `get_object` method with the todo list query set as a parameter. We then store the todo list in the `object` attribute and return the value returned by the default method. We define a `get_queryset` method that returns the tasks associated with the todo list. And we add the todo list to the template context in the `get_context_data` method. Since `CreateView` already has `SingleObjectMixin` as a base class, we just make a create view for tasks by modifying `views.py` like this:
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView

from .forms import TaskForm, TodoListForm
from .models import Task, TodoList


# Classes
# =======
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
        form.instance.todo_list = self.object
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("todo-list", args=(self.kwargs["pk"],))
```

The `get_success_url` method is used to dynamically generate the URL to redirect to. We also need to add a view which dispatches HTTP GET requests to `TodoListDetailView` and HTTP POST requests to `TaskCreateView`:
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView

from .forms import TaskForm, TodoListForm
from .models import Task, TodoList


# Classes
# =======
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
        form.instance.todo_list = self.object
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
```

Next we need to modify `simple_todo/todo_list/urls.py` like this:
```python
from django.urls import path

from . import views


urlpatterns = [
    path("", views.TodoListsView.as_view(), name="todo-lists"),
    path("todo-lists/<int:pk>/", views.TodoListView.as_view(), name="todo-list")
]
```

The URL pattern for our todo list view has a URL parameter called `pk` which will be used to pass the primary key of the todo list we want the view. We also need to open `simple_todo/todo_list/templates/todo_list/todo_lists.html` and modify it like this:
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

`{% url 'todo-list' todo_list.pk %}` is used to generate the correct URL for the todo list based on the name of the todo list detail view and the primary key of the referenced todo list. If you visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) at this point and click the name of a todo list you should now see this page:
![todo list detail view](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/13-todo_list_detail.png?raw=true)
