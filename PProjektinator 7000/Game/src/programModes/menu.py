from .programMode import ProgramMode
from src.model.modelMenu import ModelMenu
from src.view.viewMenu import ViewMenu
from src.controller.controllerMenu import ControllerMenu


class Menu(ProgramMode):

    def __init__(self):
        #super(Menu, self).__init__()
        self.model = ModelMenu()
        self.view = ViewMenu()
        self.controller = ControllerMenu()

    def processInput(self):
        pass

    def update(self):
        pass

    def render(self):
        pass