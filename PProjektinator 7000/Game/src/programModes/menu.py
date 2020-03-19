from .programMode import ProgramMode
from src.model.modelMenu import ModelMenu
from src.view.viewMenu import ViewMenu
from src.controller.controllerMenu import ControllerMenu
import pygame as py


#klasa reprezentująca menu główne gry
class Menu(ProgramMode):

    def __init__(self):
        self._model = ModelMenu()

        #menu główne ustala początkową rozdzielczość ekranu (możliwa zmiana w przyszłości na wczytywanie zapisanych ustawień z pliku)
        display = py.display.set_mode((1600, 900))
        self._view = ViewMenu(display)

        self._controller = ControllerMenu()