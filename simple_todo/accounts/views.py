from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import redirect, render

from .forms import LoginForm, RegistrationForm


# Views
# =====
def register(request):
    # Redirect automatically if already logged in
    if request.user.is_authenticated:
        url = request.GET.get("next", "/")
        return redirect(url)

    # Create registration form
    form = RegistrationForm()

    # Process submitted form data
    if request.method == "POST":
        # Validate form data
        form = RegistrationForm(request.POST)

        if form.is_valid():
            # Create user account
            try:
                user = User.objects.create_user(
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password"]
                )

            except IntegrityError:
                # Redisplay registration form
                return render(
                    request,
                    "accounts/register.html",
                    {
                        "err_msg": "The username you chose is already taken. Please choose a different username and try again.",
                        "form": RegistrationForm()
                    }
                )

            # Log in automatically
            login(request, user)

            # Redirect to the URL passed via the `next` query param
            url = request.GET.get("next", "/")
            return redirect(url)

    # Send account registration form
    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )
