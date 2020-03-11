from .programMode import ProgramMode
from src.model.modelMenu import ModelMenu
from src.view.viewMenu import ViewMenu
from src.controller.controllerMenu import ControllerMenu
import pygame as py


class Menu(ProgramMode):

    def __init__(self):
        #super(Menu, self).__init__()
        self.model = ModelMenu()

        display = py.display.set_mode((1600, 900))
        self.view = ViewMenu(display)

        self.controller = ControllerMenu()

    def processInput(self):
        pass

    def update(self):
        pass

    def render(self):
        self.view.render()