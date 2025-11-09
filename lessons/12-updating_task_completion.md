# Lesson 12: Updating Task Completion

Now that we have added the ability to edit and delete tasks, we also need to add a way to mark tasks as complete/incomplete. To do this we will start by adding a checkbox beside each task. Open `simple_todo/todo_list/templates/todo_list/todo_list.html` and modify it like this:
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
                                <div class="col-1">
                                    <input class="task-checkbox" type="checkbox"{% if task.completed %} checked{% endif %} data-url="{% url 'task-completed' task.pk %}"/>
                                </div>
                                <a class="col-7 nav-link" href="{% url 'task-edit' task.pk %}">{{ task.name }}</a>
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

If you visit the details page for a todo list now, it should have a checkbox beside each task:
*screenshot*

However, checking/unchecking them will have no effect at this point. In order for them to mark tasks as complete/incomplete, we will need to implement a simple REST API and add some JavaScript which communicates with the REST API when a task is checked/unchecked. Let's start by implementing a view we can use to check/uncheck a task. Open `simple_todo/todo_list/views.py` and modify it like this:
```python
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
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
    

class TaskCompletionView(SingleObjectMixin, View):
    model = Task

    def patch(self, request, *args, **kwargs):
        # Ensure that the user is logged in
        if not self.request.user.is_authenticated:
            return HttpResponseForbidden(json.dumps({
                "error": "User not authenticated."
            }))
        
        # Verify that the content type is application/json
        if self.request.content_type != "application/json":
            return HttpResponseBadRequest(json.dumps({
                "error": "Content type must be application/json."
            }))
        
        # Parse request body
        payload = json.loads(self.request.body)

        # Update task completion state
        task = self.get_object()
        task.completed = payload["completed"]
        task.save()
        return HttpResponse(status=204)

    def get_queryset(self):
        return Task.objects.filter(todo_list__user=self.request.user)
```

Since our new view needs to update a single task, we need to use `SingleObjectMixin` as one of its base classes. This view will be used to implement a REST endpoint. Therefore we will need to base it on `View` and write our own code to handle the HTTP request. The HTTP PATCH request is most suitable for partial updates to data, so we will implement a `patch` method which will service requests to update the completion state of a task. First we will need to check if the user is logged in. If they aren't, we will send an HTTP Forbidden response with the error message encoded as JSON. Next we will check if the content type is application/json. If it isn't, we will send an HTTP Bad Request response with the error message encoded as JSON. Then we will parse the request body as JSON. We can call the `get_object` method to fetch the task we are attempting to modify. Next we need to set the new task completion state, save the data model, and return an HTTP No Content response. We also need to set the `model` attribute to our task data model class and add a `get_queryset` method which limits access to tasks owned by the current user. Next we need to map our new view to a URL:
```python
from django.urls import path

from . import views


urlpatterns = [
    path("", views.TodoListsView.as_view(), name="todo-lists"),
    path("todo-lists/<int:pk>/", views.TodoListView.as_view(), name="todo-list"),
    path("todo-lists/<int:pk>/edit/", views.TodoListUpdateView.as_view(), name="todo-list-edit"),
    path("todo-lists/<int:pk>/delete/", views.TodoListDeleteView.as_view(), name="todo-list-delete"),
    path("tasks/<int:pk>/edit/", views.TaskUpdateView.as_view(), name="task-edit"),
    path("tasks/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/completed/", views.TaskCompletionView.as_view(), name="task-completed")
]
```

Now we need to make it so clicking the checkboxes toggles the completion state of the tasks on each todo list. To do this, we will need to write JavaScript code which will be loaded by our todo list detail page. Create a folder called `simple_todo/todo_list/static/todo_list/js`. Then create `simple_todo/todo_list/static/todo_list/js/tasks.js` with the following content:
```js
document.addEventListener("DOMContentLoaded", () => {
    // Add event listeners to task completion checkboxes
    const onTaskCompletionToggle = (evt) => {
        // Send task completion update request
        fetch(evt.target.dataset.url, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                completed: evt.target.checked
            })
        })
        .then((response) => {
            // Did the request fail?
            if(response.status != 204) {
                // Read error message
                return response.json()
                .then((payload) => {
                    // Reset checkbox to previous state and display error message
                    evt.target.checked = !evt.target.checked;
                    alert(payload.error);
                });
            }
        })
        .catch((msg) => {
            // Reset checkbox to previous state and display error message
            evt.target.checked = !evt.target.checked;
            alert(msg);
        });
    };

    document.querySelectorAll(".task-checkbox").forEach((checkbox) => {
        // Add event listener to detect checkbox toggle
        checkbox.addEventListener("change", onTaskCompletionToggle);
    });
});
```

Our new JavaScript code starts by assigning an event listener for when the page finishes loading. After the page is fully loaded, it will assign an event listener to each task checkbox which will be triggered whenever its state changes. The event listener for each checkbox will send an HTTP PATCH request to the URL placed into the `data-url` attribute of the checkbox. We must set the content type for this request to application/json and send the CSRF token stored in the `csrftoken` cookie. The body of the request will contain JSON indicating if the completion state is true or false. If the response status code is 204, the request succeeded. If it is something else or if a connection error occurs, then the state of the checkbox will be reset to its previous value and an alert will be displayed. The `getCookie` function used to get the value of the `csrftoken` cookie needs to be defined in a new file called `simple_todo/layout/static/layout/js/cookie.js`:
```js
function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            // Does this cookie string begin with the name we want?
            if(cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    
    return cookieValue;
}
```

In order to load these scripts, we will need to first modify our layout template so we can add additional scripts on a per-page basis. Open `simple_todo/layout/templates/layout/layout.html` and modify it like this:
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>{{ WEBSITE_NAME }} - {% block title %}{% endblock %}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <link rel="stylesheet" href="{% static 'layout/css/bootstrap.min.css' %}"/>
        <script src="{% static 'layout/js/bootstrap.bundle.min.js' %}"></script>
        {% block scripts %}
        {% endblock %}
    </head>
    <body>
        <div class="container-fluid">
            {% block content %}
            {% endblock %}
            <br/>
            <div class="row justify-content-center">
                <div class="col-8">
                    Copyright (c) {% now 'Y' %} by {{ AUTHOR_NAME }}
                </div>
            </div>
        </div>
    </body>
</html>
```

Now we can modify `simple_todo/todo_list/templates/todo_list/todo_list.html` like this to load our new scripts:
```html
{% extends 'layout/layout.html' %}
{% load static %}

{% block title %}Todo List{% endblock %}

{% block scripts %}
    <script src="{% static 'layout/js/cookie.js' %}"></script>
    <script src="{% static 'todo_list/js/tasks.js' %}"></script>
{% endblock %}

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
                                <div class="col-1">
                                    <input class="task-checkbox" type="checkbox"{% if task.completed %} checked{% endif %} data-url="{% url 'task-completed' task.pk %}"/>
                                </div>
                                <a class="col-7 nav-link" href="{% url 'task-edit' task.pk %}">{{ task.name }}</a>
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

Now we should be able to toggle the completion state of each task by checking/unchecking its checkbox.
