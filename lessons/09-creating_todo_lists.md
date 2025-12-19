# Lesson 09: Creating Todo Lists

In order to create todo lists using the form on the homepage of our website we will need to create an additional view and modify our `TodoListView`. Open `simple-todo/simple_todo/todo_lists/views.py` and modify it like this:
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, View
from django_htmx.http import HttpResponseClientRedirect

from .forms import TodoListForm
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
```

Our new `TodoListCreateView` extends `CreateView`. It uses submitted form data to create a new todo list. The `template_name` attribute determines the template to render to display the todo list form. The `form_class` attribute determines which form class will be used. The `success_url` attribute determines what URL to redirect to on success. We override the `form_valid` method in order to associate the new todo list with the current user before saving it by calling the base `form_valid` method. The base `form_valid` method returns an `HttpResponseRedirect` object, but since we're using htmx we must instead return an `HttpResponseClientRedirect` object. This will redirect to the homepage in order to reload it instead of replacing the form with the response. We call the `get_success_url` method to get the correct URL to redirect to. If we supply a duplicate todo list name an `IntegrityError` exception will be raised. We handle this exception by setting the error message for the name field to indicate that the todo list name was a duplicate and return the value returned by the `form_invalid` method. Next, we need to modify `simple-todo/simple_todo/todo_lists/templates/todo_lists/todo_list_create_form.html` like this:
```html
<form hx-post="{% url 'todo-lists' %}" hx-swap="outerHTML">
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

We simply fill in the URL to submit the form to and add an alert to be displayed if a duplicate name was
supplied. Now you will be able to create new todo lists via the todo list form on the homepage. If you try to create a todo list with a duplicate name, you will get a message like this:
![duplicate todo list message](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/13-duplicate_todo_list_message.png?raw=true)
