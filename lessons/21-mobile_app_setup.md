# Lesson 21: Mobile App Setup

Now that we have finished our REST API we can begin creating our mobile app. Open `requirements.txt` and modify it like this:
```
Django
django-allauth
django-environ
django-htmx
djangorestframework
djangorestframework-simplejwt
httpx
kivy
```

Next, open a new terminal in Visual Studio Code and execute the following command to install the new dependencies:
```sh
pip install -r requirements.txt
```

Since the code for our mobile app will be separate from the code for our Django project, we will need to create a separate folder for it. Create a "simple_todo_mobile" folder inside your main project folder. Now we can create the main script for our mobile app. Create `simple-todo/simple_todo_mobile/main.py` with the following content:
```python
import asyncio

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager


# Main Screen Class
# =================
class MainScreen(ScreenManager):
    pass


# App Class
# =========
class SimpleTodoMobileApp(App):
    def build(self):
        return MainScreen()
    

# Entry Point
# ===========
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(SimpleTodoMobileApp().async_run())
```

Since we will be sending requests to our REST API, we will run our app in async mode. This will keep our app responsive while waiting for responses from our REST API by not blocking the UI thread. The `MainScreen` class will be the main widget for our app. It extends the `ScreenManager` class. A screen manager widget is used to manage a set of screens. The `SimpleTodoMobileApp` class is our application class. It extends the `App` class and has a `build` method which returns our main widget. The entry point for our mobile app will create a new event loop, create an instance of our application class, call the `async_run` method of our application class, and pass the returned coroutine object to the `run_until_complete` method of our event loop. Now execute the following command in the terminal to test your mobile app:
```sh
python main.py
```

You should see a blank window like this for now:
*screenshot*

Close the window for your mobile app when you are finished testing it.
