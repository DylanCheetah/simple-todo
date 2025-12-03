# Lesson 05: Allauth Theme

At the moment our login page has no theme. We can create a theme for all of the pages provided by django-allauth by overriding the default templates used for them. The easiest way to do this is to copy the default allauth layout templates to a templates folder in our accounts app. First you need to create a `simple-todo/simple_todo/accounts/templates/` folder. Next you need to copy `simple-todo/venv/Lib/site-packages/templates/allauth/` to `simple-todo/simple_todo/accounts/templates/`. Your project structure should look like this now:
```
simple-todo/
    simple_todo/
        accounts/
            migrations/
            templates/
                allauth/
                    elements/
                    layout/
            __init__.py
            admin.py
            apps.py
            models.py
            tests.py
            urls.py
            views.py
        layout/
            migrations/
            static/
                layout/
                    css/
                        bootstrap.min.css
                    js/
                        bootstrap.bundle.min.js
            templates/
                layout/
                    base.html
            __init__.py
            admin.py
            apps.py
            ctx_proc.py
            models.py
            tests.py
            views.py
        simple_todo/
            __init__.py
            asgi.py
            settings.py
            urls.py
            wsgi.py
        .env
        .env.dist
        db.sqlite
        manage.py
    venv/
    requirements.txt
```

To change the overall look of every allauth page, modify the `simple-todo/simple_todo/accounts/templates/allauth/layout/base.html` file like this:
```html
{% load i18n %}
{% load static %}
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ WEBSITE_NAME }} - {% block head_title %}{% endblock head_title %}</title>
        <link rel="stylesheet" href="{% static 'layout/css/bootstrap.min.css' %}"/>
        <script src="{% static 'layout/js/bootstrap.bundle.min.js' %}"></script>
        {% block extra_head %}
        {% endblock extra_head %}
    </head>
    <body>
        {% block body %}
            <div class="navbar navbar-expand-lg bg-body-tertiary border-bottom sticky-top">
                <div class="container-fluid">
                    <a class="navbar-brand" href="/">{{ WEBSITE_NAME }}</a>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent" aria-controls="navbarContent" aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarContent">
                        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                            {% if not user.is_authenticated %}
                                <li class="nav-item">
                                    <a class="nav-link" href="{% url 'account_signup' %}">Sign Up</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="{% url 'account_login' %}">Sign In</a>
                                </li>
                            {% else %}
                                <li class="nav-item">
                                    <form action="{% url 'account_logout' %}" method="POST">
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
                {% if messages %}
                    <div class="row justify-content-center">
                        <div class="col-8 m-2 alert alert-primary">
                            <strong>{% trans "Messages:" %}</strong>
                            <ul>
                                {% for message in messages %}<li>{{ message }}</li>{% endfor %}
                            </ul>
                        </div>
                    </div>
                {% endif %}
                <div class="row justify-content-center">
                    <div class="col-8 m-2 card bg-light">
                        <div class="card-body">
                            {% block content %}
                            {% endblock content %}
                        </div>
                    </div>
                </div>
            </div>
        {% endblock body %}
        {% block extra_body %}
        {% endblock extra_body %}
        <div class="row justify-content-center">
            <div class="col-8 m-2">Copyright (c) {% now 'Y' %} by {{ AUTHOR_NAME }}</div>
        </div>
    </body>
</html>
```

This will add basic Bootstrap styling and a simple navbar to the allauth pages. To make the buttons use Bootstrap we will need to modify `simple-todo/simple_todo/accounts/templates/allauth/elements/button.html` like this:
```html
{% load allauth %}
{% comment %} djlint:off {% endcomment %}
<{% if attrs.href %}a href="{{ attrs.href }}"{% else %}button{% endif %}
{% if attrs.form %}form="{{ attrs.form }}"{% endif %}
{% if attrs.id %}id="{{ attrs.id }}"{% endif %}
{% if attrs.name %}name="{{ attrs.name }}"{% endif %}
{% if attrs.value %}value="{{ attrs.value }}"{% endif %}
{% if attrs.type %}type="{{ attrs.type }}"{% endif %}
class="btn btn-primary"
>
{% slot %}
{% endslot %}
</{% if attrs.href %}a{% else %}button{% endif %}>
```

To make form controls use Bootstrap styling we will need to modify `simple-todo/simple_todo/accounts/templates/allauth/elements/field.html` like this:
```html
{% load allauth %}
{{ attrs.errors }}
<p>
    {% if attrs.type == "textarea" %}
        <label for="{{ attrs.id }}">
            {% slot label %}
            {% endslot %}
        </label>
        <textarea {% if attrs.required %}required{% endif %}
                  {% if attrs.rows %}rows="{{ attrs.rows }}"{% endif %}
                  {% if attrs.disabled %}disabled{% endif %}
                  {% if attrs.readonly %}readonly{% endif %}
                  {% if attrs.checked %}checked{% endif %}
                  {% if attrs.name %}name="{{ attrs.name }}"{% endif %}
                  {% if attrs.id %}id="{{ attrs.id }}"{% endif %}
                  {% if attrs.placeholder %}placeholder="{{ attrs.placeholder }}"{% endif %}
                  class="form-control">{% slot value %}{% endslot %}</textarea>
    {% else %}
        {% if attrs.type != "checkbox" and attrs.type != "radio" %}
            <label for="{{ attrs.id }}">
                {% slot label %}
                {% endslot %}
            </label>
        {% endif %}
        <input {% if attrs.required %}required{% endif %}
               {% if attrs.disabled %}disabled{% endif %}
               {% if attrs.readonly %}readonly{% endif %}
               {% if attrs.checked %}checked{% endif %}
               {% if attrs.name %}name="{{ attrs.name }}"{% endif %}
               {% if attrs.id %}id="{{ attrs.id }}"{% endif %}
               {% if attrs.placeholder %}placeholder="{{ attrs.placeholder }}"{% endif %}
               {% if attrs.autocomplete %}autocomplete="{{ attrs.autocomplete }}"{% endif %}
               {% if attrs.value is not None %}value="{{ attrs.value }}"{% endif %}
               type="{{ attrs.type }}"
               {% if attrs.type != "checkbox" and attrs.type != "radio" %}
                   class="form-control"
               {% else %}
                   class="form-check-input"
               {% endif %}>
        {% if attrs.type == "checkbox" or attrs.type == "radio" %}
            <label for="{{ attrs.id }}">
                {% slot label %}
                {% endslot %}
            </label>
        {% endif %}
    {% endif %}
    {% if slots.help_text %}
        <span>
            {% slot help_text %}
            {% endslot %}
        </span>
    {% endif %}
</p>
```

If you view http://127.0.0.1:8000/accounts/login/ in a web browser now, it should look like this:
![user login theme v1](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/03-user_login_theme_v1.png?raw=true)

If it doesn't, try restarting the development server and refreshing the page. Notice that the page looks much better now, but the form controls don't appear to be using Bootstrap styling. This is because any controls rendered by a form class will need to be modified to use Bootstrap styling. To do this, we will need to override the default allauth form classes. Create `simple-todo/simple_todo/accounts/forms.py` with the following content:
```python
from allauth.account import forms


# Form Classes
# ============
class LoginForm(forms.LoginForm):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Add Bootstrap styling to the form fields
        self.fields["login"].widget.attrs.update({"class": "form-control"})
        self.fields["password"].widget.attrs.update({"class": "form-control"})
        self.fields["remember"].widget.attrs.update({"class": "form-check-input"})


class SignupForm(forms.SignupForm):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Add Bootstrap styling to the form fields
        self.fields["email"].widget.attrs.update({"class": "form-control"})
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


class AddEmailForm(forms.AddEmailForm):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Add Bootstrap styling to the form fields
        self.fields["email"].widget.attrs.update({"class": "form-control"})


class ChangePasswordForm(forms.ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Add Bootstrap styling to the form fields
        self.fields["oldpassword"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


class SetPasswordForm(forms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Add Bootstrap styling to the form fields
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


class ResetPasswordForm(forms.ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Add Bootstrap styling to the form fields
        self.fields["email"].widget.attrs.update({"class": "form-control"})


class ResetPasswordKeyForm(forms.ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        # Call the base constructor
        super().__init__(*args, **kwargs)

        # Add Bootstrap styling to the form fields
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})
```

Then add the following section to `simple-todo/simple_todo/simple_todo/settings.py`:
```python
# Allauth form classes
ACCOUNT_FORMS = {
    "login": "accounts.forms.LoginForm",
    "signup": "accounts.forms.SignupForm",
    "add_email": "accounts.forms.AddEmailForm",
    "change_password": "accounts.forms.ChangePasswordForm",
    "set_password": "accounts.forms.SetPasswordForm",
    "reset_password": "accounts.forms.ResetPasswordForm",
    "reset_password_from_key": "accounts.forms.ResetPasswordKeyForm"
}
```

Now if you view http://127.0.0.1:8000/accounts/login/ you should see this:
![user login theme v2](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/04-user_login_theme_v2.png?raw=true)
