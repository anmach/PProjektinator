from abc import ABC, abstractmethod
from src.enum.command import Command
import pygame as py


#klasa bazowa reprezentująca kontroler w MVC
class Controller(ABC):

    def __init__(self):
        self._command = Command.CONTINUE
        self._controls = []

    #metoda pozwalająca pobrać kontrolki z widoku (do sprawdzenia interakcji użytkownika z nimi)
    @abstractmethod
    def getControls(self, view):
        pass

    #główna metoda przetwarzająca i interpretująca dane wejściowe od użytkownika
    @abstractmethod
    def processInput(self):
        pass

    #metoda pozwalająca przekazać model do widoku w celu jego wyrenderowania
    @abstractmethod
    def communicateMV(self, model, view):
        pass

    #metoda pozwalająca na przekazanie polecenia do modelu
    @abstractmethod
    def giveCommand(self, model):
        pass

    #v----SETTERY----v

    def setCommand(self, command):
        self._command = command