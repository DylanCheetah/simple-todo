# Lesson 11: Create Login Page

Now that the registration page is working, let's make the login page. Open `simple_todo/accounts/forms.py` and add the following code:
```python
class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, widget=forms.TextInput({"class": "form-control"}))
    password = forms.CharField(min_length=8, max_length=128, widget=forms.TextInput({"class": "form-control", "type": "password"}))
```

Next, create `simple_todo/accounts/templates/accounts/login.html` with the following content:
```html
{% extends "accounts/layout.html" %}

{% block title %}Simple Todo - Login{% endblock %}

{% block content %}
    <div class="container-fluid">
        <div class="row justify-content-center">
            <h1 class="col-10">Login</h1>
        </div>
        {% if err_msg %}
            <div class="row justify-content-center">
                <div class="col-10 alert alert-danger">{{ err_msg }}</div>
            </div>
        {% endif %}
        <div class="row justify-content-center">
            <div class="col-10 card text-bg-light">
                <form class="card-body" method="post">
                    {% csrf_token %}
                    {{ form }}
                    <input class="mt-2 btn btn-primary" type="submit" value="Login">
                </form>
            </div>
        </div>
    </div>
{% endblock %}
```

Then, open `simple_todo/accounts/views.py` and add the following code:
```python
def login_view(request):
    # Automatically redirect if the user is already logged in
    if request.user.is_authenticated:
        url = request.GET.get("next", "/")
        return redirect(url)

    # Create login form
    form = LoginForm()

    # Process submitted form data
    if request.method == "POST":
        # Validate form data
        form = LoginForm(request.POST)

        if form.is_valid():
            # Authenticate user
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )

            if user is None:
                # Redisplay form
                return render(
                    request,
                    "accounts/login.html",
                    {
                        "err_msg": "The supplied credentials were invalid. Please try again.",
                        "form": LoginForm()
                    }
                )
            
            # Log the user in and redirect
            login(request, user)
            url = request.GET.get("next", "/")
            return redirect(url)

    # Send login form
    return render(
        request,
        "accounts/login.html",
        {
            "form": form
        }
    )
```

Next, open `simple_todo/accounts/urls.py` and modify it like this:
```python
from django.urls import path

from .views import login_view, register


# Create URL mappings
urlpatterns = [
    path("register/", register, name="account-register"),
    path("login/", login_view, name="account-login")
]
```

Now you should be able to execute `python manage.py runserver` and visit [http://localhost:8000/accounts/login/](http://localhost:8000/accounts/login/) to view the login page. If you are already logged in, you will be redirected to the hompage. In that case, log out via the admin site first. You should see the following page:
TODO

If you try to log in with invalid credentials, you should see this page:
TODO

And if you log in successfully, you should get redirected to the homepage:
TODO
