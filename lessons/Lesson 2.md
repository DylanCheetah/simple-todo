# Lesson 2: Project Setup

Once you have installed the prerequisties, you can start setting up a new project. First, create a folder for your new project. I'll be naming my project folder `simple-todo` but you can use any name you prefer. You can also setup source control and CI/CD at this point if you wish. However, I will not be covering that topic in this tutorial. Before we get started, we will need to create a virtual environment and install Django into it:
01. open your project folder in Visual Studio Code
02. click Terminal > New Terminal
03. create a new virtual environment
    * Windows: execute `python -m venv venv`
    * Linux: execute `python3 -m venv venv`
    * MacOS: execute `python3 -m venv venv`
04. activate virtual environment
    * Windows: execute `cmd /k venv\Scripts\activate`
    * Linux: execute `source venv/bin/activate`
    * MacOS: execute `source venv/bin/activate`
05. create `requirements.txt` with the following content:
```
Django
```
06. execute `pip install -r requirements.txt`

Note: From this point onward, you will need to activate the virtual environment in each new terminal you open.

Now that we have insalled Django into our virtual environment, we can create a new Django project for our todo list by executing the following command:
```sh
django-admin startproject simple_todo
```

Note: Django project names can only contain alphanumeric characters and underscores.

Afterwards, our project structure should look like this:
```
simple-todo/
    simple_todo/
        simple_todo/
            __init__.py
            asgi.py
            settings.py
            urls.py
            wsgi.py
        manage.py
    venv/
    requirements.txt
```

`django-admin` automatically creates a new folder for our Django project. Inside will be a `manage.py` script which is used to manage the Django project. There will also be a sub-folder with the same name as the project which contains a few scripts needed by all Django projects.
