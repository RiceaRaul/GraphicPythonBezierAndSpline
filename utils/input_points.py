from typing import Callable

from bokeh.models.widgets import TextInput, Button, Div
from bokeh.layouts import Row, Column
from bokeh.events import ButtonClick

class InputPoints:
    def __init__(self, callback: Callable | None = None):
        self.callback = callback
        self._createInputs()
    
    def _createInputs(self) -> None:
        self.label = Div(text=f"<b>Adauga un punct manual</b>")
        self.x_input = TextInput(title="Introdu valoarea lui x.", value="")
        self.y_input = TextInput(title="Introdu valoarea lui y.", value="")
        self.add_button = Button(label="Adauga")
        self.add_button.on_event(ButtonClick, self.callback)
        self.input_group_row = Row(self.x_input, self.y_input, self.add_button)
        self.input_group = Column(self.label, self.input_group_row)
    
    def get_input_group(self) -> Column:
        return self.input_group
    
    def get_x_value(self) -> str:
        return self.x_input.value
    
    def get_y_value(self) -> str:
        return self.y_input.value
        
        