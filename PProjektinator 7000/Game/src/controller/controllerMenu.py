from src.controller.controller import Controller
from src.model.modelMenu import ModelMenu
from src.view.viewMenu import ViewMenu

class ControllerMenu(Controller):

    def processInput(self):
        pass

    def communicateMV(self, model, view):
        pass

    def getControls(self, view):
        pass

    def giveCommand(self, model):
        model.setCommand(self.command)