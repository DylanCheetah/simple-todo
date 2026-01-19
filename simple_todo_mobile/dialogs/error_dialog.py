from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.popup import Popup


# Error Popup Class
# =================
class ErrorPopup(Popup):
    msg = StringProperty()


Builder.load_file("dialogs/error_dialog.kv")
