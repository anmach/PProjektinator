from .programMode import ProgramMode
from src.model.modelLevel import ModelLevel
from src.controller.controllerLevel import ControllerLevel
from src.view.viewLevel import ViewLevel

class Level(ProgramMode):
    """Gra na poziomie"""

    def __init__(self, display, level_number):
        self._model = ModelLevel(level_number, display)
        self._controller = ControllerLevel()
        self._view = ViewLevel(display)     
        
        self._controller.set_blink(self._view)

    def run(self):
        super().run()
        return (self._model.level_number, self._model.is_won())

    def change_mode(self): # <<-- TODO?
        pass
