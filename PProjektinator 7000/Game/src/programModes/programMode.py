from abc import ABC, abstractmethod
from src.model.model import Model
from src.view.view import View
from src.controller.controller import Controller


#klasa bazowa trybów programu takich jak Menu, Edytor poziomów, Gra
class ProgramMode(ABC):

    runMode = True

    def __init__(self):
        self.model = Model()
        self.view = View()
        self.controller = Controller()
    

    def run(self):
        while self.runMode :
            self.controller.getControls(self.view)
            self.controller.processInput()

            self.controller.giveCommand(self.model)
            self.model.update()

            self.controller.communicateMV(self.model, self.view)
            self.view.render()


    @abstractmethod
    def processInput(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass