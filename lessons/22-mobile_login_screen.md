# Lesson 22: Mobile Login Screen

The first screen we will need to create for our mobile app is the login screen. This will be the first screen shown when we start our mobile app. First let's create a file to store configuration variables for our mobile app. Create `simple-todo/simple_todo_mobile/config.py` with the following content:
```python
# URLs
LOGIN_URL = "http://127.0.0.1:8000/api/v1/token/"
SIGNUP_URL = "http://127.0.0.1:8000/accounts/signup/"
```

Next, create a folder called "screens" inside `simple-todo/simple_todo_mobile/` and then create `simple-todo/simple_todo_mobile/screens/login_screen.kv` with the following content:
```kvlang
#:kivy 1.9.3

<LoginScreen>:
    name: "LoginScreen"
    username: username.text
    password: password.text

    AnchorLayout:
        anchor_x: "center"
        anchor_y: "center"

        BoxLayout:
            size_hint: .5, .4
            spacing: dp(8)
            orientation: "vertical"

            Label:
                text: "Login"
                font_size: dp(24)

            TextInput:
                id: username
                hint_text: "Username"
                multiline: False

            TextInput:
                id: password
                hint_text: "Password"
                multiline: False
                password: True

            Label:
                text: root.status_msg

            Button:
                id: login_btn
                text: "Login"
                on_release: root.login()

            Button:
                id: signup_btn
                text: "Sign-Up"
                on_release: root.signup()
```

Our login screen will have a vertical box layout containing a title label, a username text input, a password text input, a status message label, a login button, and a sign-up button. The box layout will be centered inside an anchor layout. Then create `simple-todo/simple_todo_mobile/screens/login_screen.py` with the following content:
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
        # TODO: Switch to todo lists page

    def signup(self):
        # Open the user sign-up page in a web browser
        webbrowser.open(config.SIGNUP_URL)


Builder.load_file("screens/login_screen.kv")
```

The Python class for our login screen extends the `Screen` class. It has properties for the username, password, and status message. The `login` method simply schedules the `async_login` method to be executed on the event loop by calling the `spawn_task` method of our app object which we will also need to define. Our `async_login` method disables the login and sign-up buttons, sends the user credentials to the login endpoint, clears the username and password fields, enables the login and sign-up buttons, and sets the status message based on the response. If the user successfully logged in, the access and refresh tokens will be stored in the `tokens` property of our app object which we will need to define. Notice that we must manually load the .kv file which correspond with this file by calling `Builder.load_file`. The `signup` method simply opens the user sign-up page in a web browser. Now we need to modify `simple-todo/simple_todo_mobile/main.py` like this:
```python
import asyncio

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager

import screens.login_screen


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

The new `tokens` property of our app class will store the access and refresh tokens for the current user. The `spawn_task` method will create a task on the event loop. We also need to create `simple-todo/simple_todo_mobile/simpletodomobile.kv` with the following content:
```kvlang
#:kivy 1.9.3

<MainScreen>:
    LoginScreen:
```

This will add the login screen to the main screen. Since this file has the same name as our app it will be automatically loaded on startup. Also, any screens we import into `main.py` will be available in this file. If we run our mobile app at this point, it should look like this:
![mobile login screen](https://github.com/DylanCheetah/simple-todo/blob/main/lessons/screenshots/27-mobile_login_screen.png?raw=true)
