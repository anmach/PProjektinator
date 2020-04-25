from .model import Model
from src.enum.command import Command
from src.enum.editingMode import EditingMode
import os
import pygame as py


class ModelLevelEditor(Model):

    def __init__(self):
        super().__init__()

        #pobranie informacji o utworzonych już poziomach
        #       v-----inaczej nie działa-----v
        for (_, _, file_list) in os.walk('.\\saves\\levels'):
            self.__level_list = file_list

        #nr aktualnie wybranego, edytowanego poziomu
        self.__chosen_level = -1

        #wyświetlany nr poziomu do edycji (zmieniany za pomocą przycisków)
        self.__level_to_edit = 0

        #współrzędne punktów nowej platformy
        self.__new_platform_coords = (-1, -1)

        #czy aktualnie jest przemieszczany obiekt (tylko w trybie MOVE_OR_DELETE)
        self.__isMoved = False

        #aktualny tryb pracy
        self.__mode = EditingMode.NONE

    #metoda aktualizująca stan wewnętrzego modelu programu
    def update(self):
        #self.__mode = EditingMode.PLATFORM_CREATION
        if self._command == Command.EXIT:
            self._runMode = False

        elif self._command == Command.PREV_LEVEL and self.__level_to_edit > 0:
            self.__level_to_edit -= 1

        elif self._command == Command.NEXT_LEVEL and self.__level_to_edit < (len(self.__level_list) - 1):
            self.__level_to_edit += 1

        elif self._command == Command.EDIT and len(self.__level_list) > 0:
            self.__chosen_level = self.__level_to_edit
            #wczytanie nowego poziomu

        elif self._command == Command.CREATE_NEW:
            pass
            #utworzenie nowego poziomu i wczytanie go

        elif self._command == Command.SAVE and self.__chosen_level != -1:
            pass
            #zapisanie aktualnie modyfikowanego poziomu

        #interpretacja akcji użytkownika zależy od trybu w znajduje się edytor
        elif self.__mode != EditingMode.NONE:

            #lewy przycisk myszki
            if self._command == Command.CLICKED_LMB:
            
                #tworzenie nowej platformy
                if self.__mode == EditingMode.PLATFORM_CREATION:
                    #TODO
                    #sprawdzenie czy nie nachodzi/koliduje z innymi obiektami
                    #albo i bez tego, gdyż wtedy można [łatwiej] robić platformy, które nie są prostokątami
                    #może przyczepianie się do już istniejącej?
            
                    if self.__new_platform_coords == (-1, -1):
                        self.__new_platform_coords = py.mouse.get_pos()
                    else:
                        #TODO
                        #dodanie nowej platformy o współrzędnych wierzchołków [tworzących przekątną] - (self.__newPlatformCoords, py.mouse.get_pos())

                        self.__new_platform_coords = (-1, -1)
            
                elif self.__mode == EditingMode.OBJECT_PLACEMENT:
                    #TODO
                    #sprawdzenie kolizji i dodanie do poziomu
                    pass

                elif self.__mode == EditingMode.MOVE_OR_DELETE:
                    #TODO
                    #przeniesienie trzymanej rzeczy
                    if self.__isMoved == True:
                        pass
                    #sprawdzenie na co wskazuje kursor i "chwycenie tego"
                    else:
                        pass
            
            #prawy przycisk myszki
            elif self._command == Command.CLICKED_RMB:

                #w trybie tworzenia platformy
                if self.__mode == EditingMode.PLATFORM_CREATION:

                    #ale bez wierzchołków - wychodzimy z tego trybu
                    if self.__new_platform_coords == (-1, -1):
                        self.__mode = EditingMode.NONE

                    #już z jednym wierzchołkiem - usuwamy go
                    else:
                        self.__new_platform_coords = (-1, -1)

                #w trybie wstawianie nowego obiektu
                elif self.__mode == EditingMode.OBJECT_PLACEMENT:
                    self.__mode == EditingMode.NONE

    #v----GETTERY----v
    def get_level_to_edit_number(self):
        return self.__level_to_edit

    def get_new_platform_coords(self):
        return self.__new_platform_coords

    def get_mode(self):
        return self.__mode
