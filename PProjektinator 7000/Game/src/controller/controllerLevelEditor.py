from .controller import Controller
from src.enum.command import Command
import pygame as py

class ControllerLevelEditor(Controller):

    def __init__(self):
        super().__init__()
        self.__image_buttons = []

    #metoda pozwalająca pobrać kontrolki z widoku (do sprawdzenia interakcji użytkownika z nimi)
    def get_controls(self, view):
        self._controls = view.get_controls()
        self.__image_buttons = view.get_image_buttons()

    #główna metoda przetwarzająca i interpretująca dane wejściowe od użytkownika
    def process_input(self):
        #domyślne polecenie (bez tego reszta poleceń może trwać za długo, gdy nie nadejdzie inne zdarzenie)
        self._command = Command.CONTINUE

        for event in py.event.get():
            #naciśnięcie X okna
            if event.type == py.QUIT:
                self._command = Command.EXIT

            #kliknięcie myszką
            elif event.type == py.MOUSEBUTTONDOWN:
                #pobranie stanu przycisków myszy
                buttons = py.mouse.get_pressed()

                #0 - LPM
                #2 - RPM
                if buttons[0]:
                    for control in self._controls:
                        #sprawdzanie czy nad daną kontrolką jest kursor
                        if control.get_is_focused():

                            #pobranie z niej polecenia
                            self._command = control.get_command()

                            #sprawdzenie czy była to kontrolka do wybrania obiektu gry
                            if self._command == Command.OBJECT_SELECTED:
                                #TODO
                                #przekazanie info o tym jaki to konkretnie obiekt (nr w tablicy? - pomysł na przyszłość - jednak inaczej)
                                for img_butt in self.__image_buttons:
                                    if control is img_butt:
                                        self._command = img_butt.get_object_info_command()
                                        return #break???
                            return #break???
                    self._command = Command.CLICKED_LMB
                elif buttons[2]:
                    self._command = Command.CLICKED_RMB
            else:
                self._command = Command.CONTINUE

    #metoda pozwalająca przekazać model do widoku w celu jego wyrenderowania
    def communicateMV(self, model, view):
        view.set_model(model.get_level_to_edit_number(), model.get_new_platform_first_vertex_pos(), model.get_new_platform_second_vertex_pos(), model.get_mode(), model.get_all_sprites(), model.get_obj_to_del_coords())
        #view.set_player(model.get_player())

    #metoda pozwalająca na przekazanie polecenia do modelu
    def give_command(self, model):
        model.set_command(self._command)
