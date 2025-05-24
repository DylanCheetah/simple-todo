# Lesson 12: Create Logout Page

The last thing we need to add to our accounts app is create the logout page. The logout page is simple. All we need to do is open `simple_todo/accounts/views.py` and add the following code:
```python
def logout_view(request):
    # Log out and redirect to the homepage
    logout(request)
    return redirect("/")
```

Then open `simple_todo/accounts/urls.py` and modify the code like this:
```python
from django.urls import path

from .views import login_view, logout_view, register


# Create URL mappings
urlpatterns = [
    path("register/", register, name="account-register"),
    path("login/", login_view, name="account-login"),
    path("logout/", logout_view, name="account-logout")
]
```

Now if we execute `python manage.py runserver` and visit [http://localhost:8000/accounts/logout/](http://localhost:8000/accounts/logout/) we should be logged out and get redirected to the homepage:
TODO
