from abc import ABC, abstractmethod
from src.enum.command import Command


#klasa bazowa reprezentująca model w MVC
class Model(ABC):

    def __init__(self):
        #ustawienie domyślnej wartości polecenia
        self._command = Command.CONTINUE

        #ustawienie domyślnej wartości zmiennej określającej stan głównej pętli aktualnego trybu programu
        self._runMode = True

        #ustawienie domuślnej wartości zmiennej określającej czy należy przejść do nowego trybu programu
        self._changeMode = False


    #metoda aktualizująca stan wewnętrzego modelu programu
    @abstractmethod
    def update(self):
        pass

    #v----GETTERY----v
    def getRunMode(self):
        return self._runMode

    def getChangeMode(self):
        return self._changeMode

    def getCommand(self):
        return self._command

    #v----SETTERY----v
    def setCommand(self, command):
        self._command = command

    def setChangeMode(self, change):
        self._changeMode = change
    