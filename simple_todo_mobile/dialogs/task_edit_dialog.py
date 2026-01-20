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
        if response.status_code != 200:
            self.show_error("Failed to update task info.")
            return
        
        # Update task info and dismiss task edit popup
        self.task.name = self.ids.name.text
        self.task.due_date = due_date.isoformat()
        self.dismiss()


Builder.load_file("dialogs/task_edit_dialog.kv")
