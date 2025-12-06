# Lesson 09: Creating Todo Lists

In order to create todo lists using the form on the homepage of our website we will need to create an additional view and modify our `TodoListView`. Open `simple-todo/simple_todo/todo_lists/views.py` and modify it like this:
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, TemplateView, View
from django_htmx.http import HttpResponseClientRedirect

from .forms import TodoListForm


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

        return HttpResponseClientRedirect(reverse("todo-lists"))
    

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

Our new `TodoListCreateView` extends `TemplateView`. A template view will automatically render the template referenced by its `template_name` attribute using the context returned by the `get_context_data` method for HTTP GET requests. But in our case, we need to handle an HTTP POST request. Therefore, we will define a `post` method which creates an instance of our todo list form using the HTTP POST data and validates the form. If the form is invalid, the todo list form will be returned to the user to be corrected. If the form is valid, the current user will be associated with the new todo list, the new todo list will be saved, and the user will be redirected to the homepage. The reason why we redirect to the homepage is to ensure that the data displayed is correct. Since we prohibit a user from having multiple todo lists with the same name, we need to handle the `IntegrityError` exception by returning the form to the user to be corrected if the supplied todo list name was a duplicate. We will also add a descriptive error message to the template context if the name was a duplicate. Next, we need to modify `simple-todo/simple_todo/todo_lists/templates/todo_lists/todo_list_create_form.html` like this:
```html
<form hx-post="{% url 'todo-lists' %}" hx-swap="outerHTML">
    {% csrf_token %}
    {% if todo_list_create_err %}
        <div class="alert alert-danger">{{ todo_list_create_err }}</div>
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

We simply fill in the URL to submit the form to and add an alert to be displayed if a duplicate name was
supplied. Now you will be able to create new todo lists via the todo list form on the homepage. If you try to create a todo list with a duplicate name, you will get a message like this:
*screenshot*
