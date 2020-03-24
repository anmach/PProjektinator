from src.model.model import Model
from src.enum.command import Command


#klasa reprezentująca model menu
class ModelMenu(Model):

    def __init__(self):
        super().__init__()

    def update(self):
        if self._command == Command.EXIT:
            self._runMode = False
        elif self._command == Command.BROWSE_LVL:
            self._changeMode = True