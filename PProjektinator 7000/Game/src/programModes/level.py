from .programMode import ProgramMode
from src.model.modelLevel import ModelLevel
from src.controller.controllerLevel import ControllerLevel
#from src.view.viewLevel import ViewLevel <-- TODO Toporze

class level(ProgramMode):
    """Gra na poziomie"""

    def __init__(self, display):
        self._controller = ControllerLevel()
        self._model = ModelLevel()
        #self._view = ViewLevel(display) <-- TODO

    def change_mode(self): # <<-- TODO?
        pass