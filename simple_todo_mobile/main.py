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
