# Lesson 27: Refresh Token

At this point we have successfully built and deployed our todo list website and companion mobile app. However, you may have noticed a slight bug in the mobile app. If you start the mobile app, log in, and leave the app idle for a few minutes you may notice that the app stops working. This is because the access token obtained by the app will expire after a set period of time. However, we can fix this by having the mobile app automatically obtain a new access token by using the refresh token. To do this we will first need to add a new method to our app class in `simple-todo/simple_todo_mobile/main.py`:
```python
import asyncio
import httpx

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager

import config
import screens.login_screen
import screens.todo_lists_screen
import screens.todo_list_screen


# Main Screen Class
# =================
class MainScreen(ScreenManager):
    pass


# App Class
# =========
class SimpleTodoMobileApp(App):
    tokens = ObjectProperty()
    
    def build(self):
        return MainScreen()
    
    def spawn_task(self, coro):
        loop.create_task(coro)

    async def refresh_token(self):
        # Request a new access token
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{config.LOGIN_URL}refresh/",
                    json={
                        "refresh": self.tokens["refresh"]
                    }
                )

            except httpx.ConnectError:
                return False
            
        # Check status code
        if response.status_code != 200:
            return False
        
        # Update access token
        self.tokens["access"] = response.json()["access"]
        return True
    

# Entry Point
# ===========
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(SimpleTodoMobileApp().async_run())
```

The `refresh_token` method will use the refresh token to receive a new access token. Next we need to modify `simple-todo/simple_todo_mobile/screens/todo_lists_screen.py` like this:
```python
import httpx
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import (
    ListProperty, 
    NumericProperty, 
    ObjectProperty, 
    StringProperty
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, SlideTransition

import config
from dialogs.error_dialog import ErrorPopup


# Todo List Class
# ===============
class TodoList(BoxLayout):
    id = NumericProperty()
    name = StringProperty()
    delete = ObjectProperty()
    view = ObjectProperty()

    def on_touch_up(self, touch):
        # Was the label touched?
        if self.ids.name_label.collide_point(touch.x, touch.y):
            self.view(self.id)


# Todo Lists Screen Class
# =======================
class TodoListsScreen(Screen):
    new_todo_list_name = StringProperty()
    next_page = StringProperty()
    todo_lists = ListProperty()
    scroll_y = NumericProperty()
    scrollable_dist = NumericProperty()
    dist_to_top = NumericProperty()

    def on_enter(self):
        # Reset todo lists screen
        self.reset()

    def on_scroll_y(self, instance, value):
        # Calculate distance to top
        self.dist_to_top = (1 - self.scroll_y) * self.scrollable_dist

        # Have we reached the bottom of the todo lists view?
        if value == 0.0:
            # Load next page of todo lists
            self.load_next_page()

    def on_scrollable_dist(self, instance, value):
        # Set new scroll pos
        self.ids.todo_lists.scroll_y = (
            (self.scrollable_dist - self.dist_to_top) / self.scrollable_dist)

    def reset(self):
        # Clear todo lists and schedule todo lists load task
        self.next_page = config.TODO_LISTS_URL
        self.todo_lists = []
        self.load_next_page()

    def show_error(self, msg):
        # Show error popup
        popup = ErrorPopup(msg=msg)
        popup.open()

    def load_next_page(self):
        # Schedule todo lists load task
        App.get_running_app().spawn_task(self.async_load_next_page())

    async def async_load_next_page(self):
        # Return if there isn't a next page
        if self.next_page == "":
            return

        # Load next page of todo lists
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.next_page,
                    headers={
                        "Authorization": f"Bearer {App.get_running_app().tokens['access']}"
                    }
                )

            except httpx.ConnectError:
                self.show_error("Network connection failed.")
                return
            
        # Check status code
        if response.status_code == 403:
            # Refresh access token
            if not await App.get_running_app().refresh_token():
                self.show_error("Failed to refresh access token.")
                return
            
            # Retry request
            await self.async_load_next_page()
            return

        elif response.status_code != 200:
            self.show_error("Failed to fetch todo lists.")
            return
        
        # Load todo list data
        payload = response.json()
        self.next_page = payload["next"] if payload["next"] is not None else ""
        self.todo_lists = (
            self.todo_lists + 
            [
                {
                    "id": todo_list["id"], 
                    "name": todo_list["name"], 
                    "delete": self.delete_todo_list,
                    "view": self.view_todo_list
                } for todo_list in payload["results"]
            ]
        )

    def create_todo_list(self):
        # Schedule todo list create task
        App.get_running_app().spawn_task(self.async_create_todo_list())

    async def async_create_todo_list(self):
        # Disable todo list create button
        self.ids.create_todo_list_btn.disabled = True

        # Create new todo list
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    config.TODO_LISTS_URL,
                    headers={
                        "Authorization": f"Bearer {App.get_running_app().tokens['access']}"
                    },
                    json={
                        "name": self.new_todo_list_name
                    }
                )

            except httpx.ConnectError:
                self.show_error("Network connection failed.")
                return
            
            finally:
                # Enable todo list create button
                self.ids.create_todo_list_btn.disabled = False
            
        # Check status code
        if response.status_code == 403:
            # Refresh access token
            if not await App.get_running_app().refresh_token():
                self.show_error("Failed to refresh access token.")
                return
            
            # Retry request
            await self.async_create_todo_list()
            return

        elif response.status_code != 201:
            self.show_error("Failed to create todo list.")
            return
        
        # Clear new todo list name field and refresh todo lists
        self.ids.new_todo_list_name.text = ""
        self.reset()

    def delete_todo_list(self, id):
        # Schedule todo list deletion
        App.get_running_app().spawn_task(self.async_delete_todo_list(id))

    async def async_delete_todo_list(self, id):
        # Delete the todo list which corresponds with the given ID
        async with httpx.AsyncClient() as client:
            try:
                response = await client.delete(
                    f"{config.TODO_LISTS_URL}{id}/",
                    headers={
                        "Authorization": f"Bearer {App.get_running_app().tokens['access']}"
                    }
                )

            except httpx.ConnectError:
                self.show_error("Network connection failed.")
                return
            
        # Check status code
        if response.status_code == 403:
            # Refresh access token
            if not await App.get_running_app().refresh_token():
                self.show_error("Failed to refresh access token.")
                return
            
            # Retry request
            await self.async_delete_todo_list()
            return

        elif response.status_code != 204:
            self.show_error("Failed to delete todo list.")
            return
        
        # Refresh todo lists
        self.reset()

    def view_todo_list(self, id):
        # Set the todo list to view and switch to the todo list screen
        self.parent.get_screen("TodoListScreen").todo_list = id
        self.parent.transition = SlideTransition(direction="left")
        self.parent.current = "TodoListScreen"


Builder.load_file("screens/todo_lists_screen.kv")
```

The new code will cause the mobile app to refresh the access token and retry any request which fails with 403 Unauthorized. Then we need to modify `simple-todo/simple_todo_mobile/screens/todo_list_screen.py` like this:
```python
from datetime import datetime

import httpx
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import (
    ListProperty, 
    NumericProperty, 
    ObjectProperty, 
    StringProperty
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import NoTransition, Screen, SlideTransition

import config
from dialogs.error_dialog import ErrorPopup
from dialogs.task_edit_dialog import TaskEditPopup


# Task Class
# ==========
class Task(BoxLayout):
    id = NumericProperty()
    name = StringProperty()
    due_date = StringProperty()
    edit = ObjectProperty()
    delete = ObjectProperty()

    def format_date(self, s):
        # If the date string is empty, return it unmodified
        if s == "":
            return s
        
        # Format the date string
        date = datetime.fromisoformat(s)
        return date.strftime("%m/%d/%Y %H:%M")


# Todo List Screen Class
# ======================
class TodoListScreen(Screen):
    todo_list = NumericProperty()
    todo_list_name = StringProperty()
    next_page = StringProperty()
    tasks = ListProperty()
    scrollable_dist = NumericProperty()
    dist_to_top = NumericProperty()
    scroll_y = NumericProperty()

    def on_scroll_y(self, instance, value):
        # Calculate new distance to top
        self.dist_to_top = (1 - self.scroll_y) * self.scrollable_dist

        # If we're at the bottom of the list, load the next page of tasks
        if self.scroll_y == 0.0:
            self.load_next_page()

    def on_scrollable_dist(self, instance, value):
        # Calculate new scroll position
        self.scroll_y = (
            (self.scrollable_dist - self.dist_to_top) / self.scrollable_dist)

    def on_todo_list(self, instance, value):
        # Schedule todo list info load
        App.get_running_app().spawn_task(self.async_load_todo_list_info())

    def show_error(self, msg):
        # Show error popup
        popup = ErrorPopup(msg=msg)
        popup.open()

    async def async_load_todo_list_info(self):
        # Return if the todo list is 0
        if not self.todo_list:
            return

        # Load todo list info
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{config.TODO_LISTS_URL}{self.todo_list}/",
                    headers={
                        "Authorization": f"Bearer {App.get_running_app().tokens['access']}"
                    }
                )

            except httpx.ConnectError:
                self.show_error("Network connection failed.")
                return

        # Check status code
        if response.status_code == 403:
            # Refresh access token
            if not await App.get_running_app().refresh_token():
                self.show_error("Failed to refresh access token.")
                return
            
            # Retry request
            await self.async_load_todo_list_info()
            return

        elif response.status_code != 200:
            self.show_error("Failed to fetch todo list info.")
            return

        # Set todo list name
        payload = response.json()
        self.todo_list_name = payload["name"]

        # Reset todo list screen
        self.reset()

    def back(self):
        # Return to todo lists screen
        self.parent.transition = SlideTransition(direction="right")
        self.parent.current = "TodoListsScreen"

    def edit(self):
        # Show edit form
        self.ids.todo_list_info.transition = NoTransition()
        self.ids.todo_list_info.current = "TodoListForm"

    def save(self):
        # Schedule todo list save
        App.get_running_app().spawn_task(self.async_save())

    async def async_save(self):
        # Disable todo list save button and cancel edit button
        self.ids.save_todo_list_btn.disabled = True
        self.ids.cancel_edit_btn.disabled = True

        # Save todo list info
        async with httpx.AsyncClient() as client:
            try:
                response = await client.put(
                    f"{config.TODO_LISTS_URL}{self.todo_list}/",
                    headers={
                        "Authorization": f"Bearer {App.get_running_app().tokens['access']}"
                    },
                    json={
                        "name": self.ids.todo_list_name.text
                    }
                )

            except httpx.ConnectError:
                self.show_error("Network connection failed.")
                return
            
            finally:
                # Enable todo list save button and cancel edit button
                self.ids.save_todo_list_btn.disabled = False
                self.ids.cancel_edit_btn.disabled = False
            
        # Check status code
        if response.status_code == 403:
            # Refresh access token
            if not await App.get_running_app().refresh_token():
                self.show_error("Failed to refresh access token.")
                return
            
            # Retry request
            await self.async_save()
            return

        elif response.status_code != 200:
            self.show_error("Failed to update todo list info.")
            return
        
        # Set todo list name and hide todo list form
        self.todo_list_name = self.ids.todo_list_name.text
        self.ids.todo_list_info.current = "TodoListInfo"

    def cancel_edit(self):
        # Hide edit form
        self.ids.todo_list_info.transtion = NoTransition()
        self.ids.todo_list_info.current = "TodoListInfo"

    def reset(self):
        # Set the next page URL, clear the tasks, and load the next page of tasks
        self.next_page = f"{config.TASKS_URL}?todo_list={self.todo_list}"
        self.tasks = []
        self.load_next_page()

    def load_next_page(self):
        # Schedule task load task
        App.get_running_app().spawn_task(self.async_load_next_page())

    async def async_load_next_page(self):
        # Return if there isn't a next page
        if self.next_page == "":
            return
        
        # Fetch tasks
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.next_page,
                    headers={
                        "Authorization": f"Bearer {App.get_running_app().tokens['access']}"
                    }
                )

            except httpx.ConnectError:
                self.show_error("Network connection failed.")
                return
            
        # Check status code
        if response.status_code == 403:
            # Refresh access token
            if not await App.get_running_app().refresh_token():
                self.show_error("Failed to refresh access token.")
                return
            
            # Retry request
            await self.async_load_next_page()
            return
        
        elif response.status_code != 200:
            self.show_error("Failed to fetch tasks.")
            return
        
        # Set next page URL and display additional tasks
        payload = response.json()
        self.next_page = payload["next"] if payload["next"] is not None else ""
        self.tasks = self.tasks + [
            {
                "id": task["id"],
                "name": task["name"],
                "due_date": task["due_date"],
                "edit": self.edit_task, 
                "delete": self.delete_task
            } for task in payload["results"]
        ]

    def create_task(self):
        # Schedule task create task
        App.get_running_app().spawn_task(self.async_create_task())

    async def async_create_task(self):
        # Disable task create button
        self.ids.create_task_btn.disabled = True

        # Create new task
        async with httpx.AsyncClient() as client:
            try:
                due_date = datetime.strptime(
                    self.ids.new_task_due_date.text, 
                    config.DATE_FORMAT).astimezone()
                response = await client.post(
                    config.TASKS_URL,
                    headers={
                        "Authorization": f"Bearer {App.get_running_app().tokens['access']}"
                    },
                    json={
                        "todo_list": self.todo_list, 
                        "name": self.ids.new_task_name.text,
                        "due_date": due_date.isoformat()
                    }
                )

            except httpx.ConnectError:
                self.show_error("Network connection failed.")
                return
            
            except ValueError:
                self.show_error("Invalid due date.")
                return
            
            finally:
                # Enable task create button
                self.ids.create_task_btn.disabled = False

        # Check status code
        if response.status_code == 403:
            # Refresh access token
            if not await App.get_running_app().refresh_token():
                self.show_error("Failed to refresh access token.")
                return
            
            # Retry request
            await self.async_create_task()
            return
        
        elif response.status_code != 201:
            self.show_error("Failed to create task.")
            return
        
        # Clear new task fields and refresh tasks
        self.ids.new_task_name.text = ""
        self.ids.new_task_due_date.text = ""
        self.reset()

    def edit_task(self, task):
        # Show task edit popup
        popup = TaskEditPopup(
            task=task,
            name=task.name,
            due_date=task.due_date
        )
        popup.open()

    def delete_task(self, id):
        # Schedule task deletion
        App.get_running_app().spawn_task(self.async_delete_task(id))

    async def async_delete_task(self, id):
        # Delete the task associated with the given ID
        async with httpx.AsyncClient() as client:
            try:
                response = await client.delete(
                    f"{config.TASKS_URL}{id}/",
                    headers={
                        "Authorization": f"Bearer {App.get_running_app().tokens['access']}"
                    }
                )

            except httpx.ConnectError:
                self.show_error("Network connection failed.")
                return
            
        # Check status code
        if response.status_code == 403:
            # Refresh access token
            if not await App.get_running_app().refresh_token():
                self.show_error("Failed to refresh access token.")
                return
            
            # Retry request
            await self.async_delete_task()
            return
        
        elif response.status_code != 204:
            self.show_error("Failed to delete task.")
            return
        
        # Refresh tasks view
        self.reset()


Builder.load_file("screens/todo_list_screen.kv")
```

We also need to modify `simple-todo/simple_todo_mobile/dialogs/task_edit_dialog.py` like this:
```python
from datetime import datetime

import httpx
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup

import config
from dialogs.error_dialog import ErrorPopup


# Task Edit Popup Class
# =====================
class TaskEditPopup(Popup):
    task = ObjectProperty()
    name = StringProperty()
    due_date = StringProperty()

    def format_date(self, s):
        # If the date string is empty, return it unmodified
        if s == "":
            return s
        
        # Format the date string
        date = datetime.fromisoformat(s)
        return date.strftime("%m/%d/%Y %H:%M")
    
    def show_error(self, msg):
        # Show error popup
        popup = ErrorPopup(msg=msg)
        popup.open()

    def update_task(self):
        # Schedule task update
        App.get_running_app().spawn_task(self.async_update_task())

    async def async_update_task(self):
        # Disable save and cancel buttons
        self.ids.save_task_btn.disabled = True
        self.ids.cancel_edit_task_btn.disabled = True

        # Update task data
        async with httpx.AsyncClient() as client:
            try:
                due_date = datetime.strptime(
                    self.ids.due_date.text, 
                    config.DATE_FORMAT).astimezone()
                response = await client.patch(
                    f"{config.TASKS_URL}{self.task.id}/",
                    headers={
                        "Authorization": f"Bearer {App.get_running_app().tokens['access']}"
                    },
                    json={
                        "name": self.ids.name.text, 
                        "due_date": due_date.isoformat()
                    }
                )

            except httpx.ConnectError:
                self.show_error("Network connection failed.")
                return
            
            except ValueError:
                self.show_error("Invalid due date.")
                return
            
            finally:
                # Enable save and cancel buttons
                self.ids.save_task_btn.disabled = False
                self.ids.cancel_edit_task_btn.disabled = False
            
        # Check status code
        if response.status_code == 403:
            # Refresh access token
            if not await App.get_running_app().refresh_token():
                self.show_error("Failed to refresh access token.")
                return
            
            # Retry request
            await self.async_update_task()
            return
        
        elif response.status_code != 200:
            self.show_error("Failed to update task info.")
            return
        
        # Update task info and dismiss task edit popup
        self.task.name = self.ids.name.text
        self.task.due_date = due_date.isoformat()
        self.dismiss()


Builder.load_file("dialogs/task_edit_dialog.kv")
```

Now our mobile app should automatically refresh the access token as needed.
