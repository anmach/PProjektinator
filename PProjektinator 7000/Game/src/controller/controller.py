from abc import ABC, abstractmethod
from src.enum.command import Command

class Controller(ABC):

    def __init__(self):
        self.command = Command.CONTINUE

    @abstractmethod
    def getControls(self, view):
        pass

    @abstractmethod
    def processInput(self):
        pass

    @abstractmethod
    def communicateMV(self, model, view):
        pass

    @abstractmethod
    def giveCommand(self, model):
        pass