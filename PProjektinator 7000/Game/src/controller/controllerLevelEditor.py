from .controller import Controller
from src.enum.command import Command
import pygame as py

class ControllerLevelEditor(Controller):

    def __init__(self):
        super().__init__()

    #metoda pozwalająca pobrać kontrolki z widoku (do sprawdzenia interakcji użytkownika z nimi)
    def get_controls(self, view):
        self._controls = view.get_controls()

    #główna metoda przetwarzająca i interpretująca dane wejściowe od użytkownika
    def process_input(self):
        #domyślne polecenie (bez tego reszta poleceń może trwać za długo, gdy nie nadejdzie inne zdarzenie)
        self._command = Command.CONTINUE

        for event in py.event.get():
            #naciśnięcie X okna
            if event.type == py.QUIT:
                self._command = Command.EXIT

            #kliknięcie myszką
            if event.type == py.MOUSEBUTTONDOWN:

                #pobranie stanu przycisków myszy
                buttons = py.mouse.get_pressed()

                #0 - LPM
                #2 - RPM
                if buttons[0]:
                    self._command = Command.CLICKED_LMB
                elif buttons[2]:
                    self._command = Command.CLICKED_RMB

                for control in self._controls:
                    #sprawdzanie czy nad daną kontrolką jest kursor
                    if control.get_is_focused():
                        #pobranie z niej polecenia
                        self._command = control.get_command()
            else:
                self._command = Command.CONTINUE

    #metoda pozwalająca przekazać model do widoku w celu jego wyrenderowania
    def communicateMV(self, model, view):
        view.set_model(model.get_level_to_edit_number(), model.get_new_platform_coords(), model.get_mode())

    #metoda pozwalająca na przekazanie polecenia do modelu
    def give_command(self, model):
        model.set_command(self._command)
