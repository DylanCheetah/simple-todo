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
        # TODO: Switch to todo lists page

    def signup(self):
        # Open the user sign-up page in a web browser
        webbrowser.open(config.SIGNUP_URL)


Builder.load_file("screens/login_screen.kv")
