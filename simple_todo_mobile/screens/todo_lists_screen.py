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
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

import config


# Todo List Class
# ===============
class TodoList(BoxLayout):
    id = NumericProperty()
    name = StringProperty()
    delete = ObjectProperty()


# Error Popup Class
# =================
class ErrorPopup(Popup):
    msg = StringProperty()


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
