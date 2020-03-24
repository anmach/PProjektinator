from .programMode import ProgramMode
from src.model.modelLevelBrowser import ModelLevelBrowser
from src.view.viewLevelBrowser import ViewLevelBrowser
#from src.controller.controllerMenu import ControllerMenu


class LevelBrowser(ProgramMode):

    def __init__(self, display):
        self._model = ModelLevelBrowser()

    def changeMode(self):
        pass