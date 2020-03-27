from .controller import Controller
from src.model.modelLevelBrowser import ModelLevelBrowser
from src.enum.command import Command
import pygame as py


class ControllerLevelBrowser(Controller):
    
    def __init__(self):
        super().__init__()

    #metoda pozwalająca pobrać kontrolki z widoku (do sprawdzenia interakcji użytkownika z nimi)
    def get_controls(self, view):
        self._controls = view.get_controls()

    #główna metoda przetwarzająca i interpretująca dane wejściowe od użytkownika
    def process_input(self):
        for event in py.event.get():

            #naciśnięcie X okna
            if event.type == py.QUIT:
                self._command = Command.EXIT

            #kliknięcie myszką
            if event.type == py.MOUSEBUTTONDOWN:
                for control in self._controls:
                    #sprawdzanie czy nad daną kontrolką jest kursor
                    if control.get_is_focused():
                        #pobranie z niej polecenia
                        self._command = control.get_command()

    #metoda pozwalająca przekazać model do widoku w celu jego wyrenderowania
    def communicateMV(self, model, view):
        view.set_shown_level(model.get_shown_level_number())

    #metoda pozwalająca na przekazanie polecenia do modelu
    def give_command(self, model):
        model.set_command(self._command)