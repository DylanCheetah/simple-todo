from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
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
    def delete(self, request, *args, **kwargs):
        # Dispatch to the todo list delete view
        view = TodoListDeleteView.as_view()
        return view(request, *args, **kwargs)
