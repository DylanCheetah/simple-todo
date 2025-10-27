# Lesson 8: Homepage

Now that we have user registration and authentication setup for our todo list web app, we can create the homepage for our application. The homepage will consist of 2 sections. The first section will be a form for creating new todo lists. The second section will show a list of the todo lists which belong to the current user. Let's start by creating the template for the page. Create a `simple_todo/todo_list/templates/todo_list` folder for your templates and create `simple_todo/todo_list/templates/todo_list/todo_lists.html` with the following content:
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
                                <a class="col-10 nav-link" href="">{{ todo_list.name }}</a>
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

`{% for todo_list in todo_lists %}` is used to iterate over the `todo_lists` context variable. `{% empty %}` is used to define content to be displayed when the length of the object list is 0. `{% endfor %}` is used to end the for loop. Notice that we can use the `if`, `else`, and `endif` Django tags to render different blocks of HTML depending on the value of context variables. For now we will leave the href for each todo list and its delete button blank. Create `simple_todo/todo_list/forms.py` with the following content:
```python
from django import forms

from .models import TodoList


# Classes
# =======
class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ["name"]
        widgets = {
            "name": forms.CharField(attrs={"class": "form-control"})
        }
```

Our `TodoListForm` class should extend `ModelForm`. Inside should be an inner `Meta` class. The `model` attribute of the meta class should be set to the todo list model class. The `fields` attribute of the meta class should be set to the names of the fields which should be displayed in the form. The `widgets` attribute of the meta class should be set to a dictionary which provides a custom widget for each field. We will enable Bootstrap styling by setting the class of the `name` field to "form-control". Now we can create the view for our homepage. Since our homepage is used both to create and display todo lists, we will need to create both a `CreateView` sub-class and a `ListView` sub-class. Open `simple_todo/todo_list/views.py` and modify it like this:
```python
from django.shortcuts import render
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
```

In our `TodoListListView` class we need to set the template name. We will also set the `paginate_by` attribute to 10 in order to control the number of todo lists which can be displayed per page. The `get_queryset` method should return the objects we need to display. The `get_context_data` method should get the context from the base method and add a `TodoListForm` instance to it before returning the context. In our `TodoListCreateView` class we need to set the `model` attribute to our todo list model and we also need to set the `form_class` attribute to our todo list form class. The `form_valid` method associates the new todo list with the current user before calling the base method. Both classes should have `LayoutMixin` in their base class list. The next thing we need to do is associate both views with the same URL. We will do this by creating a third view. The third view will subclass `View` and `LoginRequiredMixin`:
```python
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
```

The `TodoListView` class has `LoginRequiredMinxin` as a base class to require users to be logged in to view the homepage. Inside the `TodoListView` class we need to set the `login_url` attribute to the path of our login page. The `get` method calls `as_view` on our `TodoListListView` class to instanciate the view and then calls the view with the same parameters it received. The `post` method does the same with the `TodoListCreateView`. Now we need to map our todo list view to a URL. Create `simple_todo/todo_list/urls.py` with the following content:
```python
from django.urls import path

from . import views


urlpatterns = [
    path("", views.TodoListView.as_view(), name="todo-lists")
]
```

We also need to modify `simple_todo/simple_todo/urls.py` like this:
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("todo_list.urls")),
    path("accounts/", include("accounts.urls")),
    path('admin/', admin.site.urls),
]
```

If we visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in a web browser we will be redirected to the login page if we aren't already logged in. Otherwise, we will see the homepage:
*screenshot*
