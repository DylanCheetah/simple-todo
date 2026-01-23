from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView


# View Classes
# ============
class AccountDeleteView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/account_delete.html"

    def post(self, *args, **kwargs):
        # Delete the current user's account and return to the homepage
        self.request.user.delete()
        messages.add_message(
            self.request, 
            messages.INFO, 
            "Your account has been successfully deleted."
        )
        return HttpResponseRedirect(reverse("todo-lists"))
