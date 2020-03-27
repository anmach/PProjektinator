from .programMode import ProgramMode
from .levelBrowser import LevelBrowser
from src.model.modelMenu import ModelMenu
from src.view.viewMenu import ViewMenu
from src.controller.controllerMenu import ControllerMenu
from src.enum.command import Command
import pygame as py


class Menu(ProgramMode):
    """klasa reprezentująca menu główne gry"""

    def __init__(self):
        self._model = ModelMenu()

        #menu główne ustala początkową rozdzielczość ekranu (możliwa zmiana w przyszłości na wczytywanie zapisanych ustawień z pliku)
        display = py.display.set_mode((1600, 900))
        self._view = ViewMenu(display)

        self._controller = ControllerMenu()

    def change_mode(self):
        #przejście do przeglądarki poziomów
        if(self._model.get_command() == Command.BROWSE_LVL):
            print(self._model.get_command())
            levelBrowser = LevelBrowser(self._view.get_surface())
            levelBrowser.run()
            self._controller.set_command(Command.CONTINUE)