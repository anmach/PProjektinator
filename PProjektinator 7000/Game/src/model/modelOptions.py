from src.model.model import Model
from src.enum.command import Command

class ModelOptions(Model):
    """klasa reprezentująca model menu opcji"""

    def __init__(self):
        super().__init__()

    def update(self):
        if self._command == Command.EXIT:
            self._runMode = False

