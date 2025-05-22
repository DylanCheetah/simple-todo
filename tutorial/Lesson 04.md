# Lesson 04: Setup Unit Testing

Before we proceed, we will setup unit testing for our backend so we can track what parts of our backend are working correctly and what needs to be fixed. First, create a new Django app called "api" by executing the following command:
```sh
python manage.py startapp api
```

Then open `simple_todo/simple_todo/settings.py` and add `api` to the list of installed apps:
```python
INSTALLED_APPS = [
    "api",
    "rest_framework",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Next, open `simple_todo/api/tests.py` and modify it like this:
```python
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task, TodoList


# Unit Test Classes
# =================
class TodoListTests(APITestCase):
    def test_create_todo_list(self):
        # Create test user
        user = User.objects.create_user(
            username="Tester",
            password="test"
        )

        # Create todo list via REST API
        self.client.force_login(user)
        response = self.client.post(
            "/api/v1/todo-lists/",
            {
                "name": "Test"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_todo_list(self):
        # Create test todo lists
        user, user2, _, _ = create_test_todo_lists()

        # Read todo lists via REST API
        self.client.force_login(user)
        response = self.client.get("/api/v1/todo-lists/")
        self.assertEqual(len(response.json()["results"]), 1)

        response = self.client.get("/api/v1/todo-lists/1/")
        self.assertEqual(response.json()["name"], "Test")

    def test_update_todo_list(self):
        # Create test todo lists
        user, user2, _, _ = create_test_todo_lists()

        # Update todo list via REST API
        self.client.force_login(user)
        response = self.client.put(
            "/api/v1/todo-lists/1/",
            {
                "name": "NewTest"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Try to update other user's todo list
        response = self.client.put(
            "/api/v1/todo-lists/2/",
            {
                "name": "NewTest"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_todo_list(self):
        # Create test todo lists
        user, user2, _, _ = create_test_todo_lists()

        # Delete todo list via REST API
        self.client.force_login(user)
        response = self.client.delete("/api/v1/todo-lists/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Try to delete other user's todo list
        response = self.client.delete("/api/v1/todo-lists/2/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TaskTests(APITestCase):
    def test_create_task(self):
        # Create test todo lists
        user, user2, todo_list, todo_list2 = create_test_todo_lists()

        # Create task via REST API
        self.client.force_login(user)
        response = self.client.post(
            "/api/v1/tasks/",
            {
                "todo_list": todo_list.id,
                "name": "wash the dishes"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_task(self):
        # Create test tasks
        user, user2, todo_list, todo_list2 = create_test_tasks()

        # Read tasks via REST API
        self.client.force_login(user)
        response = self.client.get("/api/v1/tasks/")
        self.assertEqual(len(response.json()["results"]), 2)

        response = self.client.get("/api/v1/tasks/?todo_list=1")
        self.assertEqual(len(response.json()["results"]), 1)

        response = self.client.get("/api/v1/tasks/1/")
        self.assertEqual(response.json()["name"], "wash the dishes")

    def test_update_task(self):
        # Create test tasks
        user, user2, todo_list, todo_list2 = create_test_tasks()

        # Update task via REST API
        self.client.force_login(user)
        response = self.client.put(
            "/api/v1/tasks/1/",
            {
                "name": "wash the car"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Try to update other user's task too
        response = self.client.put(
            "/api/v1/tasks/3/",
            {
                "name": "wash the car"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_task(self):
        # Create test tasks
        user, user2, todo_list, todo_list2 = create_test_tasks()

        # Delete task via REST API
        self.client.force_login(user)
        response = self.client.delete("/api/v1/tasks/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Try to delete other user's task
        response = self.client.delete("/api/v1/tasks/3/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# Utility Functions
# =================
def create_test_todo_lists():
    # Create test users
    user = User.objects.create_user(
        username="Tester",
        password="test"
    )
    user2 = User.objects.create_user(
        username="Tester2",
        password="test2"
    )

    # Create test todo lists
    todo_list = TodoList.objects.create(
        owner=user,
        name="Test"
    )
    todo_list2 = TodoList.objects.create(
        owner=user2,
        name="Test"
    )

    return user, user2, todo_list, todo_list2


def create_test_tasks():
    # Create test todo lists
    user, user2, todo_list, todo_list2 = create_test_todo_lists()

    # Create test tasks
    Task.objects.create(
        todo_list=todo_list,
        name="wash the dishes"
    )
    Task.objects.create(
        todo_list=todo_list,
        name="wash the laundry"
    )
    Task.objects.create(
        todo_list=todo_list2,
        name="wash the dishes"
    )
    Task.objects.create(
        todo_list=todo_list2,
        name="wash the laundry"
    )

    return user, user2, todo_list, todo_list2
```
