from abc import ABC, abstractmethod
from src.enum.command import Command

class Model(ABC):

    def __init__(self):
        self.command = Command.CONTINUE

    def setCommand(self, command):
        self.command = command

    @abstractmethod
    def update():
        pass
    