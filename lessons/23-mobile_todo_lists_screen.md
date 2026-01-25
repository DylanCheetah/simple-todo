# Lesson 23: Mobile Todo Lists Screen

Now that we are able to log into our mobile app we can implement the screen which will display the todo lists associated with the current user. Open `simple-todo/simple_todo_mobile/config.py` and modify it like this:
```python
# URLs
LOGIN_URL = "http://127.0.0.1:8000/api/v1/token/"
SIGNUP_URL = "http://127.0.0.1:8000/accounts/signup/"
TODO_LISTS_URL = "http://127.0.0.1:8000/api/v1/todo-lists/"
```

Next, create a folder called "dialogs" inside `simple-todo/simple_todo_mobile/` and create `simple-todo/simple_todo_mobile/dialogs/error_dialog.kv` with the following content:
```kvlang
#:kivy 1.9.3

<ErrorPopup>:
    title: "Error"
    msg: ""

    BoxLayout:
        orientation: "vertical"

        Label:
            size_hint_y: .9
            text: root.msg

        Button:
            size_hint_y: .1
            text: "Ok"
            on_release: root.dismiss()
```

Then create `simple-todo/simple_todo_mobile/error_dialog.py` with the following content:
```python
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.popup import Popup


# Error Popup Class
# =================
class ErrorPopup(Popup):
    msg = StringProperty()


Builder.load_file("dialogs/error_dialog.kv")
```

This dialog box will be used to display any error messages which occur. Next, create `simple-todo/simple_todo_mobile/screens/todo_lists_screen.kv` with the following content:
```kvlang
#:kivy 1.9.3

<TodoList>:
    id: 0
    name: ""
    delete: None

    Label:
        size_hint_x: .8
        text: root.name

    Button:
        size_hint_x: .2
        text: "Delete"
        on_release: root.delete(root.id)


<TodoListsScreen>:
    name: "TodoListsScreen"
    new_todo_list_name: new_todo_list_name.text
    todo_lists: []
    scroll_y: todo_lists.scroll_y
    scrollable_dist: todo_lists_layout.height - todo_lists.height

    BoxLayout:
        padding: dp(8)
        orientation: "vertical"

        BoxLayout:
            size_hint_y: .2
            spacing: dp(8)
            orientation: "vertical"

            Label:
                text: "New Todo List"
                font_size: dp(24)

            BoxLayout:
                Label:
                    size_hint_x: .2
                    text: "Name:"

                TextInput:
                    id: new_todo_list_name
                    size_hint_x: .8
                    multiline: False

            Button:
                id: create_todo_list_btn
                text: "Create"
                on_release: root.create_todo_list()

        BoxLayout:
            size_hint_y: .8
            spacing: dp(8)
            orientation: "vertical"

            Label:
                size_hint_y: .1
                text: "Todo Lists"
                font_size: dp(24)

            RecycleView:
                id: todo_lists
                size_hint_y: .9
                viewclass: "TodoList"
                data: root.todo_lists

                RecycleBoxLayout:
                    id: todo_lists_layout
                    orientation: "vertical"
                    spacing: dp(8)
                    default_size: None, dp(56)
                    default_size_hint: 1, None
                    size_hint_y: None
                    height: self.minimum_height
```

The our todo lists screen will consist of 2 box layouts inside a main box layout. The top box layout will contain a label, the fields needed to create a todo list, and a button to create a new todo list. The bottom box layout will contain a label and a recycle view which will display the todo lists owned by the current user. We will also need a todo list widget which will be used to display each todo list in the recycle view. Now we need to create `simple-todo/simple_todo_mobile/screens/todo_lists_screen.py` with the following content:
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
from kivy.uix.screenmanager import Screen

import config
from dialogs.error_dialog import ErrorPopup


# Todo List Class
# ===============
class TodoList(BoxLayout):
    id = NumericProperty()
    name = StringProperty()
    delete = ObjectProperty()


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
        if response.status_code != 200:
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
                    "delete": self.delete_todo_list
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
        if response.status_code != 201:
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
        if response.status_code != 204:
            self.show_error("Failed to delete todo list.")
            return
        
        # Refresh todo lists
        self.reset()


Builder.load_file("screens/todo_lists_screen.kv")
```

The `TodoListsScreen` class contains properties for the fields needed to create a new todo list, a property for the next page URL, a property for the loaded todo lists, a property for the scroll position of the recycle view, a property for the scrollable distance of the recycle view, and a property for the distance to the top of the recycle view. The `on_enter` method will reset the todo lists screen when we switch to it. The `on_scroll_y` method will calculate the current distance to the top of the recycle view and load the next page of todo lists whenever we reach the bottom of the loaded todo lists. The `on_scrollable_dist` method will recalculate the scroll position of the recycle view whenver the scrollable distance changes. The `reset` method resets the next page URL, clears the loaded todo lists, and loads the next page of todo lists. The `show_error` method creates an error popup and displays it. The `load_next_page` method schedules the `async_load_next_page` method. The `async_load_next_page` method fetches the next page of todo lists, sets the new next page URL, and adds the fetched todo lists to the list of todo lists. The `create_todo_list` method schedules the `async_create_todo_list` method. The `async_create_todo_list` method creates a new todo list and refreshes the todo lists recycle view. The `delete_todo_list` method schedules the `async_delete_todo_list` method. The `async_delete_todo_list` method deletes a todo list and refreshes the todo lists recycle view. Next we need to modify `simple-todo/simple_todo_mobile/main.py` like this:
```python
import asyncio

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager

import screens.login_screen
import screens.todo_lists_screen


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
    

# Entry Point
# ===========
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(SimpleTodoMobileApp().async_run())
```

We also need to add our new screen to `simple-todo/simple_todo_mobile/simpletodomobile.kv`:
```kvlang
#:kivy 1.9.3

<MainScreen>:
    LoginScreen:
    TodoListsScreen:
```

And we need to modify `simple-todo/simple_todo_mobile/screens/login_screen.py` like this:
```python
import webbrowser

import httpx
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

import config


# Login Screen Class
# ==================
class LoginScreen(Screen):
    username = StringProperty()
    password = StringProperty()
    status_msg = StringProperty()

    def login(self):
        # Spawn login task
        App.get_running_app().spawn_task(self.async_login())

    async def async_login(self):
        # Disable login and sign-up buttons
        self.ids.login_btn.disabled = True
        self.ids.signup_btn.disabled = True

        # Send login request
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    config.LOGIN_URL,
                    json={
                        "username": self.username,
                        "password": self.password
                    }
                )

            except httpx.ConnectError:
                self.status_msg = "Network Error"
                return

            finally:
                # Clear username and password fields
                self.ids.username.text = ""
                self.ids.password.text = ""

                # Enable login and sign-up buttons
                self.ids.login_btn.disabled = False
                self.ids.signup_btn.disabled = False
        
        # Check for errors
        if response.status_code == 401:
            self.status_msg = "Invalid User Credentials"
            return

        elif response.status_code != 200:
            print(response.status_msg)

        # Clear status message, store tokens, and switch to todo lists page
        self.status_msg = ""
        App.get_running_app().tokens = response.json()
        self.parent.current = "TodoListsScreen"

    def signup(self):
        # Open the user sign-up page in a web browser
        webbrowser.open(config.SIGNUP_URL)


Builder.load_file("screens/login_screen.kv")
```

If you run the mobile app now you should be able to view your todo lists, created new todo lists, and delete existing todo lists. If you scroll to the bottom of the loaded todo lists, additional todo lists will be loaded if there are more:
![mobile todo lists screen](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/28-mobile_todo_lists_screen.png?raw=true)
