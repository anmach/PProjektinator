from .programMode import ProgramMode
from src.model.modelLevelEditor import ModelLevelEditor
from src.controller.controllerLevelEditor import ControllerLevelEditor
from src.view.viewLevelEditor import ViewLevelEditor


class LevelEditor(ProgramMode):

    def __init__(self, display):
        self._model = ModelLevelEditor()
        self._view = ViewLevelEditor(surface)
        self._controller = ControllerLevelEditor()