# Lesson 13: Navigation and Logout

As it stands, navigating our todo list web app isn't the most user-friendly. For example, if a user is viewing the details of a todo list or on any other page they must either click the back button or type a new address into the address bar if they wish to return to the homepage. Also, they have no way to log out yet. To address these issues, we will add a navigation bar that's visible at the top of every page. To do this we will need to modify `simple_todo/layout/templates/layout/layout.html` like this:
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
        <div class="navbar navbar-expand-lg bg-body-tertiary border-bottom sticky-top">
            <div class="container-fluid">
                <a class="navbar-brand" href="{% url 'todo-lists' %}">Simple Todo</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent" aria-controls="navbarContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarContent">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        {% if not user.is_authenticated %}
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'user-create' %}">Register</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'user-login' %}">Login</a>
                            </li>
                        {% else %}
                            <li class="nav-item">
                                <form method="POST" action="{% url 'user-logout' %}">
                                    {% csrf_token %}
                                    <input class="nav-link" type="submit" value="Logout"/>
                                </form>
                            </li>
                        {% endif %}
                    </ul>
                </div>
            </div>
        </div>
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

The new HTML code adds a Bootstrap navbar to the top of the page which will remain stuck to the top of the window even when the user scrolls the page. It has a branding link which shows the name of the app and can be clicked to return to the homepage. When the user is not logged in, it will show Register and Login links on the navbar. When the user is logged in, it will show a Logout link which submits a logout form to our `UserLogoutView`. The web interface for our todo list web app is now complete. In the next lesson, we will start implementing a progressive web app version of our todo list web app.
