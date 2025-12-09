# Lesson 10: Deleting Todo Lists

In order to delete todo lists we will need to create a new view and map it to a URL which accepts the primary key of the todo list to delete as a URL parameter. For convenience, we can also use this URL when we add the ability to view and edit individual todo lists. So we will go ahead and create 2 new views. One view will handle deleting a todo list and the other will dispatch HTTP DELETE requests to the todo list delete view. Open `simple-todo/simple_todo/todo_lists/views.py` and modify it like this:
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView, TemplateView, View
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
    

class TodoListDeleteView(View):
    def get_queryset(self):
        return self.request.user.todo_lists.all()

    def delete(self, request, *args, **kwargs):
        # Delete the requested todo list
        todo_list = get_object_or_404(self.get_queryset(), pk=kwargs["pk"])
        todo_list.delete()
        return HttpResponseClientRedirect(reverse("todo-lists"))


class TodoListView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        # Dispatch to the todo list delete view
        view = TodoListDeleteView.as_view()
        return view(request, *args, **kwargs)
```

The `get_object_or_404` function accepts a queryset and the same arguments as the `get` method of the `objects` attribute of a data model class. If the requested data model instance isn't found, it will raise an `Http404` exception. If the requested todo list is found, its `delete` method will be called to delete it. Next we need to map our new view to a URL. Open `simple-todo/simple_todo/todo_lists/urls.py` and modify it like this:
```python
from django.urls import path

from . import views


urlpatterns = [
    path("", views.TodoListsView.as_view(), name="todo-lists"),
    path("todo_lists/<int:pk>/", views.TodoListView.as_view(), name="todo-list")
]
```

Now we need to make it so clicking the delete button beside each todo list deletes the todo list. Whenever we need to modify the data associated with our website, we must supply a CSRF token. Therefore, we need to change our delete button so that it is inside a form with a CSRF token. However, since we will be using an HTTP DELETE request to delete a todo list we need to pass the CSRF token in the "X-CSRFToken" header instead of in the request body. Open `simple-todo/simple_todo/todo_lists/templates/todo_lists/todo_lists_partial.html` and modify it like this:
```html
<div id="todo_lists-view">
    {% for todo_list in page_obj %}
        <div class="row">
            <div class="col m-1 card bg-light">
                <div class="card-body row">
                    <a class="col-10 nav-link" href="">{{ todo_list.name }}</a>
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

The `hx-delete` attribute determines the URL to submit the HTTP DELETE request to when we click the delete button. The `hx-headers` attribute is set to a single-quoted string of JSON data which defines additional HTTP headers to send with the request. The `csrf_token` template context variable contains the CSRF token we need to send along with the request.
