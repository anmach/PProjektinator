from .model import Model
from src.enum.command import Command
import os


class ModelLevelEditor(Model):

    def __init__(self):
        super().__init__()

        #pobranie informacji o utworzonych już poziomach
        #       v-----inaczej nie działa-----v
        for (_, _, fileList) in os.walk('.\\saves\\levels'):
            self.__levelList = fileList

        #nr aktualnie wybranego, edytowanego poziomu
        self.__chosenLevel = -1

        #wyświetlany nr poziomu do edycji (zmieniany za pomocą przycisków)
        self.__levelToEdit = 0

        #współrzędne punktów nowej platformy
        self.__newPlatformPoints = []

    #metoda aktualizująca stan wewnętrzego modelu programu
    @abstractmethod
    def update(self):
        if self._command == Command.EXIT:
            self._runMode = False

        elif self._command == Command.PREV_LEVEL and self.__levelToEdit > 0:
            self.__levelToEdit -= 1

        elif self._command == Command.NEXT_LEVEL and self.__levelToEdit < (len(self.__levelList) - 1):
            self.__levelToEdit += 1

        elif self._command == Command.EDIT and len(self.__levelList) > 0:
            self.__chosenLevel = self.__levelToEdit
            #wczytanie nowego poziomu

        elif self._command == Command.CREATE_NEW:
            pass
            #utworzenie nowego poziomu i wczytanie go

        elif self._command == Command.SAVE and self.__chosenLevel != -1:
            pass
            #zapisanie aktualnie modyfikowanego poziomu
