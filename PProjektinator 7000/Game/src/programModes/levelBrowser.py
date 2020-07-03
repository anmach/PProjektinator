from .programMode import ProgramMode
from .level import Level
from src.model.modelLevelBrowser import ModelLevelBrowser
from src.view.viewLevelBrowser import ViewLevelBrowser
from src.controller.controllerLevelBrowser import ControllerLevelBrowser
from src.enum.command import Command

class LevelBrowser(ProgramMode):

    def __init__(self, display):
        self._model = ModelLevelBrowser()
        self._view = ViewLevelBrowser(display)
        self._controller = ControllerLevelBrowser()

    def change_mode(self):
       if(self._model.get_command() == Command.PLAY):
            level = Level(self._view.get_surface(), self._model.get_shown_level_number())
            level_won = level.run()
            if level_won[1]:
                self._model.unlock_level(level_won[0])
            self._controller.set_command(Command.CONTINUE)
