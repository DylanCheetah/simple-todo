from django.contrib.auth.models import User
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
        users, todo_lists = create_test_todo_lists()

        # Read todo lists via REST API
        self.client.force_login(users[0])
        response = self.client.get("/api/v1/todo-lists/")
        self.assertEqual(len(response.json()["results"]), 2)

        response = self.client.get(f"/api/v1/todo-lists/{todo_lists[0].id}/")
        self.assertEqual(response.json()["name"], "Test")

    def test_update_todo_list(self):
        # Create test todo lists
        users, todo_lists = create_test_todo_lists()

        # Update todo list via REST API
        self.client.force_login(users[0])
        response = self.client.put(
            f"/api/v1/todo-lists/{todo_lists[0].id}/",
            {
                "name": "NewTest"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Try to update other user's todo list
        response = self.client.put(
            f"/api/v1/todo-lists/{todo_lists[2].id}/",
            {
                "name": "NewTest"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_todo_list(self):
        # Create test todo lists
        users, todo_lists = create_test_todo_lists()

        # Delete todo list via REST API
        self.client.force_login(users[0])
        response = self.client.delete(
            f"/api/v1/todo-lists/{todo_lists[0].id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Try to delete other user's todo list
        response = self.client.delete(
            f"/api/v1/todo-lists/{todo_lists[2].id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TaskTests(APITestCase):
    def test_create_task(self):
        # Create test todo lists
        users, todo_lists = create_test_todo_lists()

        # Create task via REST API
        self.client.force_login(users[0])
        response = self.client.post(
            "/api/v1/tasks/",
            {
                "todo_list": todo_lists[0].id,
                "name": "wash the dishes"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_task(self):
        # Create test tasks
        users, todo_lists = create_test_tasks()

        # Read tasks via REST API
        self.client.force_login(users[0])
        response = self.client.get("/api/v1/tasks/")
        self.assertEqual(len(response.json()["results"]), 3)

        response = self.client.get(
            f"/api/v1/tasks/?todo_list={todo_lists[1].id}")
        self.assertEqual(len(response.json()["results"]), 1)

        response = self.client.get("/api/v1/tasks/1/")
        self.assertEqual(response.json()["name"], "wash the dishes")

    def test_update_task(self):
        # Create test tasks
        users, todo_lists = create_test_tasks()

        # Update task via REST API
        self.client.force_login(users[0])
        response = self.client.put(
            f"/api/v1/tasks/1/?todo_list={todo_lists[0].id}",
            {
                "name": "wash the car"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Try to update other user's task too
        response = self.client.put(
            "/api/v1/tasks/4/",
            {
                "name": "wash the car"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_task(self):
        # Create test tasks
        users, todo_lists = create_test_tasks()

        # Delete task via REST API
        self.client.force_login(users[0])
        response = self.client.delete("/api/v1/tasks/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Try to delete other user's task
        response = self.client.delete("/api/v1/tasks/4/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# Utility Functions
# =================
def create_test_todo_lists():
    # Create test users
    users = [
        User.objects.create_user(
            username="Tester",
            password="test"
        ),
        User.objects.create_user(
            username="Tester2",
            password="test2"
        )
    ]

    # Create test todo lists
    todo_lists = [
        TodoList.objects.create(
            owner=users[0],
            name="Test"
        ),
        TodoList.objects.create(
            owner=users[0],
            name="Test2"
        ),
        TodoList.objects.create(
            owner=users[1],
            name="Test"
        )
    ]

    return users, todo_lists


def create_test_tasks():
    # Create test todo lists
    users, todo_lists = create_test_todo_lists()

    # Create test tasks
    Task.objects.create(
        todo_list=todo_lists[0],
        name="wash the dishes"
    )
    Task.objects.create(
        todo_list=todo_lists[0],
        name="wash the laundry"
    )
    Task.objects.create(
        todo_list=todo_lists[1],
        name="fold laundry"
    )
    Task.objects.create(
        todo_list=todo_lists[2],
        name="wash the dishes"
    )
    Task.objects.create(
        todo_list=todo_lists[2],
        name="wash the laundry"
    )

    return users, todo_lists
