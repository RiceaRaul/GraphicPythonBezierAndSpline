from bokeh.models import (
    Div,
    Button,
    Dialog,
)
from bokeh.layouts import Column
from bokeh.events import ButtonClick

class DialogModal:
    def __init__(self , modalmessage: str, modalvisible: bool = False):
        self.modal_message = modalmessage
        self.modal_visible = modalvisible
        self.dialog = None
        self._createModal()

    def _createModal(self) -> None:
        self.error_message = Div(text=f"<b>{self.modal_message}</b>")
        self.close_button = Button(label="Close", button_type="success")  
        self.close_button.on_event(ButtonClick, self._closeModal)
        self.dialog = Dialog(title="Error", content=Column(self.error_message, self.close_button), visible=False,draggable = True,closable = False)
        self.dialog.css_classes = ["custom-dialog"]

    def getDialog(self) -> Dialog:
        return self.dialog
    
    def openDialog(self, modalmessage: str = "") -> None:
        self.error_message.text = f"<b>{modalmessage}</b>"
        self.dialog.visible = True

    def _closeModal(self,event) -> None:
        self.dialog.visible = False
