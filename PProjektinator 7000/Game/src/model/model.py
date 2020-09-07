from abc import ABC, abstractmethod
from src.enum.command import Command


class Model(ABC):
    """klasa bazowa reprezentująca model w MVC"""

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
    def get_run_mode(self):
        return self._runMode

    def get_change_mode(self):
        return self._changeMode

    def get_command(self):
        return self._command

    #v----SETTERY----v
    def set_command(self, command):
        self._command = command
        
    def get_error(self):       
        return 1

    def set_change_mode(self, change):
        self._changeMode = change
    