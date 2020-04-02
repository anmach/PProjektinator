from .programMode import ProgramMode
from src.model.modelLevel import ModelLevel
from src.controller.controllerLevel import ControllerLevel
from src.view.viewLevel import ViewLevel

class Level(ProgramMode):
    """Gra na poziomie"""

    def __init__(self, display, level_number):
        self._model = ModelLevel(level_number)
        self._controller = ControllerLevel()
        self._view = ViewLevel(display)

    def change_mode(self): # <<-- TODO?
        pass
