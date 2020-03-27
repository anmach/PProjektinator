from .programMode import ProgramMode
from src.model.modelLevelBrowser import ModelLevelBrowser
from src.view.viewLevelBrowser import ViewLevelBrowser
from src.controller.controllerLevelBrowser import ControllerLevelBrowser


class LevelBrowser(ProgramMode):

    def __init__(self, display):
        self._model = ModelLevelBrowser()
        self._view = ViewLevelBrowser(display)
        self._controller = ControllerLevelBrowser()

    def change_mode(self):
        pass