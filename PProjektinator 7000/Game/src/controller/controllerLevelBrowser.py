from .controller import Controller
from src.model.modelLevelBrowser import ModelLevelBrowser
from src.enum.command import Command
import pygame as py


class ControllerLevelBrowser(Controller):
    
    def __init__(self):
        super().__init__()

    #metoda pozwalająca pobrać kontrolki z widoku (do sprawdzenia interakcji użytkownika z nimi)
    @abstractmethod
    def getControls(self, view):
        self._controls = view.getControls()

    #główna metoda przetwarzająca i interpretująca dane wejściowe od użytkownika
    @abstractmethod
    def processInput(self):
        for event in py.event.get():

            #naciśnięcie X okna
            if event.type == py.QUIT:
                self._command = Command.EXIT

            #kliknięcie myszką
            if event.type == py.MOUSEBUTTONDOWN:
                for control in self._controls:
                    #sprawdzanie czy nad daną kontrolką jest kursor
                    if control.getIsFocused():
                        #pobranie z niej polecenia
                        self._command = control.getCommand()

    #metoda pozwalająca przekazać model do widoku w celu jego wyrenderowania
    @abstractmethod
    def communicateMV(self, model, view):
        pass

    #metoda pozwalająca na przekazanie polecenia do modelu
    @abstractmethod
    def giveCommand(self, model):
        model.setCommand(self._command)