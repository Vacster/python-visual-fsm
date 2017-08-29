import pyperclip
from pygame import event
from constants import Custom_Event

class Input_Manager:
    def __init__(self):
        self.message = ""

    def take_input(self, char=None):
        #Ctrl-C
        if char is None or char == "":
            self.message = ""
        #Backspace
        elif char == "\b":
            self.message = self.message[:-1]
        #Enter
        elif char == "\r":
            message_split = self.message.split(" ")
            event.post(
                event.Event(Custom_Event.RUN_COMMAND, message=message_split)
            )
        #Ctrl-V
        elif char == "":
            self.message += pyperclip.paste()
        else:
            self.message += char

        event.post(
            event.Event(Custom_Event.UPDATE_INPUT_MESSAGE, message=self.message)
        )

    def get_message(self):
        return self.message
