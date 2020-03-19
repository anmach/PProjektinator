from abc import ABC, abstractmethod
from src.enum.command import Command


#klasa bazowa reprezentująca model w MVC
class Model(ABC):

    def __init__(self):
        #ustawienie domyślnej wartości polecenia
        self._command = Command.CONTINUE

        #ustawienie domyślnej zmiennej określającej stan głównej pętli aktualnego trybu programu
        self._runMode = True

    
    #metoda aktualizująca stan wewnętrzego modelu programu
    @abstractmethod
    def update():
        pass

    #v----GETTERY----v
    def getRunMode(self):
        return self._runMode

    #v----SETTERY----v
    def setCommand(self, command):
        self._command = command
    