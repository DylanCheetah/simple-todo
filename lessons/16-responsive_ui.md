# Lesson 16: Responsive UI

At this point our todo list website is functionally complete. However, we need to test how the UI looks on mobile devices. To do this we can make use of the responsive design mode built into many modern web browsers. In Brave you can enable responsive design mode by right-clicking a webpage, clicking Inspect, and clicking the Toggle Device Toolbar button in the upper left corner of the web developer tools pane. In Microsoft Edge you can enable responsive design mode by right-clicking a webpage, clicking Inspect, and clicking the Toggle Device Emulation button in the upper left corner of the web developer tools pane. The process is similar in other browsers as well. I will be using Brave. First, let's log out and see how the login page looks:
![resonsive design mode](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/17-responsive_design_mode.png?raw=true)

You will notice that on a mobile device the width of the content is quite a bit less since the screen width is less. We can fix this by defining different column widths based on screen size. Open `simple-todo/simple_todo/accounts/templates/allauth/layouts/base.html` and modify it like this:
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
            {% include "layout/navbar.html" %}
            <div class="container-fluid">
                {% if messages %}
                    <div class="row justify-content-center">
                        <div class="col-lg-8 col-md-10 col-11 m-2 alert alert-primary">
                            <strong>{% trans "Messages:" %}</strong>
                            <ul>
                                {% for message in messages %}<li>{{ message }}</li>{% endfor %}
                            </ul>
                        </div>
                    </div>
                {% endif %}
                <div class="row justify-content-center">
                    <div class="col-lg-8 col-md-10 col-11 m-2 card bg-light">
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
            <div class="col-lg-8 col-md-10 col-11 m-2">Copyright (c) {% now 'Y' %} by {{ AUTHOR_NAME }}</div>
        </div>
    </body>
</html>
```

"col-lg-8" will set the column width to 8 on large screens, "col-md-10" will set the column width to 10 on medium screens, and "col-11" will set the column width to 11 for extra small screens. This allows us to adapt the width of the content so it better fits the screen size. Refresh the page and try changing the type of device being emulated to see how it affects the content:
![responsive ui](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/18-responsive_ui.png?raw=true)

Now try logging in to see how our homepage looks on a mobile device:
![homepage on mobile](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/19-homepage_on_mobile.png?raw=true)

As you can see, our homepage looks very broken on mobile devices. Let's fix this. Open `simple-todo/simple_todo/layout/templates/layout/base.html` and modify it like this:
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>{{ WEBSITE_NAME }} - {% block title %}{% endblock %}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <link rel="stylesheet" href="{% static 'layout/css/bootstrap.min.css' %}"/>
        <script src="{% static 'layout/js/bootstrap.bundle.min.js' %}"></script>
        <script src="{% static 'layout/js/htmx.min.js' %}"></script>
    </head>
    <body>
        {% include "layout/navbar.html" %}
        <div class="container-fluid">
            {% if messages %}
                <div class="row justify-content-center">
                    <div class="col-lg-8 col-md-10 col-11 m-2 alert alert-primary">
                        <strong>Messages:</strong>
                        <ul>
                            {% for message in messages %}
                                <li>{{ message }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
            {% endif %}
            {% block content %}
            {% endblock %}
            <div class="row justify-content-center">
                <div class="col-lg-8 col-md-10 col-11 m-2">Copyright (c) {% now 'Y' %} by {{ AUTHOR_NAME }}</div>
            </div>
        </div>
    </body>
</html>
```

Next, open `simple-todo/simple_todo/todo_lists/templates/todo_lists/todo_lists_full.html` and modify it like this:
```html
{% extends "layout/base.html" %}

{% block title %}Todo Lists{% endblock %}

{% block content %}
    <div class="row justify-content-center">
        <div class="col-lg-8 col-md-10 col-11 m-2 card bg-light">
            <div class="card-body">
                <h3 class="card-title">New Todo List</h3>
                {% include "todo_lists/todo_list_create_form.html" %}
            </div>
        </div>
    </div>
    <div class="row justify-content-center">
        <div class="col-lg-8 col-md-10 col-11 m-2 card bg-light">
            <div class="card-body">
                <h3 class="card-title">Todo Lists</h3>
                {% include "todo_lists/todo_lists_partial.html" %}
            </div>
        </div>
    </div>
{% endblock %}
```

Now open `simple-todo/simple_todo/todo_lists/templates/todo_lists/todo_lists_partial.html` and modify it like this:
```html
<div id="todo_lists-view">
    {% for todo_list in page_obj %}
        <div class="row">
            <div class="col m-1 card bg-light">
                <div class="card-body row">
                    <a class="col-lg-10 col-md-9 col-7 nav-link" href="{% url 'todo-list' todo_list.pk %}">{{ todo_list.name }}</a>
                    <form class="col-lg-2 col-md-3 col-5"
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
            <button class="col-lg-2 col-md-3 col-4 btn btn-primary"
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
            <button class="col-lg-2 col-md-3 col-4 btn btn-secondary pe-none">Previous</button>
        {% endif %}
        <div class="col-lg-2 col-md-3 col-4 text-center">Page {{ page_obj.number }} of {{ paginator.num_pages }}</div>
        {% if page_obj.has_next %}
            <button class="col-lg-2 col-md-3 col-4 btn btn-primary"
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
            <button class="col-lg-2 col-md-3 col-4 btn btn-secondary pe-none">Next</button>
        {% endif %}
    </div>
</div>
```

If you refresh the page it should look better now:
![resonsive homepage](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/20-responsive_homepage.png?raw=true)

Next, try clicking one of the todo lists to see how the todo list detail page looks on mobile:
![todo list details on mobile](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/21-todo_list_details_on_mobile.png?raw=true)

We can fix this page in a similar manner. Open `simple-todo/simple_todo/todo_lists/templates/todo_lists/todo_list_full.html` and modify it like this:
```html
{% extends "layout/base.html" %}

{% block title %}Todo List Details{% endblock %}

{% block content %}
    {% include "todo_lists/todo_list_info.html" %}
    <div class="row justify-content-center">
        <div class="col-lg-8 col-md-10 col-11 m-2 card bg-light">
            <div class="card-body">
                <h3 class="card-title">New Task</h3>
                {% include "todo_lists/task_create_form.html" %}
            </div>
        </div>
    </div>
    <div class="row justify-content-center">
        <div class="col-lg-8 col-md-10 col-11 m-2 card bg-light">
            <div class="card-body">
                <h3 class="card-title">Tasks</h3>
                {% include "todo_lists/tasks_partial.html" %}
            </div>
        </div>
    </div>
{% endblock %}
```

Next, open `simple-todo/simple_todo/todo_lists/templates/todo_lists/todo_list_info.html` and modify it like this:
```html
<div id="todo_list-info" class="row justify-content-center">
    <h1 class="col-lg-8 col-md-10 col-11">
        {{ todo_list.name }}
        <button class="btn btn-warning"
            hx-get="{% url 'todo-list-edit' todo_list.pk %}"
            hx-target="#todo_list-info"
            hx-swap="outerHTML">
            <div class="spinner-border spinner-border-sm htmx-indicator">
                <span class="visually-hidden">Loading...</span>
            </div>
            Edit
        </button>
    </h1>
</div>
```

We also need to modify `simple-todo/simple_todo/todo_lists/templates/todo_lists/todo_list_update_form.html` like this:
```html
<div id="todo_list-update-form" class="row justify-content-center">
    <form class="col-lg-8 col-md-10 col-11"
          hx-post="{% url 'todo-list' todo_list.pk %}"
          hx-target="#todo_list-update-form"
          hx-swap="outerHTML">
          {% csrf_token %}
          {{ form }}
        <br/>
        <button class="m-1 btn btn-success">
            <div class="spinner-border spinner-border-sm htmx-indicator">
                <span class="visually-hidden">Loading...</span>
            </div>
            Save
        </button>
        <button class="m-1 btn btn-danger"
                type="button"
                hx-get="{% url 'todo-list-info' todo_list.pk %}"
                hx-target="#todo_list-update-form"
                hx-swap="outerHTML">
            <div class="spinner-border spinner-border-sm htmx-indicator">
                <span class="visually-hidden">Loading...</span>
            </div>
            Cancel
        </button>
    </form>
</div>
```

Next, open `simple-todo/simple_todo/todo_lists/templates/todo_lists/tasks_partial.html` and modify it like this:
```html
<div id="tasks-view">
    {% for task in page_obj %}
        <div class="row justify-content-center">
            <div class="col m-1 card bg-light">
                {% include "todo_lists/task_info.html" %}
            </div>
        </div>
    {% empty %}
        No Data
    {% endfor %}
    <br/>
    <div class="row justify-content-center">
        {% if page_obj.has_previous %}
            <button class="col-lg-2 col-md-3 col-4 btn btn-primary"
                    hx-get="{% url 'todo-list' todo_list.pk %}?page={{ page_obj.previous_page_number }}"
                    hx-target="#tasks-view"
                    hx-swap="outerHTML"
                    hx-push-url="true">
                    <div class="spinner-border spinner-border-sm htmx-indicator">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    Previous
            </button>
        {% else %}
            <button class="col-lg-2 col-md-3 col-4 btn btn-secondary pe-none">Previous</button>
        {% endif %}
        <div class="col-lg-2 col-md-3 col-4 text-center">Page {{ page_obj.number }} of {{ paginator.num_pages }}</div>
        {% if page_obj.has_next %}
            <button class="col-lg-2 col-md-3 col-4 btn btn-primary"
                    hx-get="{% url 'todo-list' todo_list.pk %}?page={{ page_obj.next_page_number }}"
                    hx-target="#tasks-view"
                    hx-swap="outerHTML"
                    hx-push-url="true">
                <div class="spinner-border spinner-border-sm htmx-indicator">
                    <span class="visually-hidden">Loading...</span>
                </div>
                Next
            </button>
        {% else %}
            <button class="col-lg-2 col-md-3 col-4 btn btn-secondary pe-none">Next</button>
        {% endif %}
    </div>
</div>
```

Now open `simple-todo/simple_todo/todo_lists/templates/todo_lists/task_info.html` and modify it like this:
```html
<div id="task-{{ task.pk }}" class="card-body row">
    <div class="col-lg-8 col-md-6 col-12">
        <div class="row">
            <div class="col-12">{{ task.name }}</div>
        </div>
        <div class="row">
            <div class="col-12 text-secondary">{{ task.due_date }}</div>
        </div>
    </div>
    <div class="col-lg-2 col-md-3 col-12 m-lg-0 m-md-0 m-1">
        <button class="col-12 btn btn-warning"
                hx-get="{% url 'task-edit' task.pk %}"
                hx-target="#task-{{ task.pk }}"
                hx-swap="outerHTML">
            <div class="spinner-border spinner-border-sm htmx-indicator">
                <span class="visually-hidden">Loading...</span>
            </div>
            Edit
        </button>
    </div>
    <form class="col-lg-2 col-md-3 col-12 m-lg-0 m-md-0 m-1"
            hx-delete="{% url 'task' task.pk %}"
            hx-target="#tasks-view"
            hx-swap="outerHTML"
            hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
        <button class="col-12 btn btn-danger">
            <div class="spinner-border spinner-border-sm htmx-indicator">
                <span class="visually-hidden">Loading...</span>
            </div>
            Delete
        </button>
    </form>
</div>
```

If you refresh the page now, it should look better:
![responsive todo list details](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/22-responsive_todo_list_details.png?raw=true)
