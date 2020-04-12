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
        for (_, _, fileList) in os.walk('.\\saves\\levels'):
            self.__levelList = fileList

        #nr aktualnie wybranego, edytowanego poziomu
        self.__chosenLevel = -1

        #wyświetlany nr poziomu do edycji (zmieniany za pomocą przycisków)
        self.__levelToEdit = 0

        #współrzędne punktów nowej platformy
        self.__newPlatformCoords = (-1, -1)

        #liczba utworzonych już wierzchołków nowej platformy
        self.__createdVerticesNumber = 0

        #aktualny tryb pracy
        self.__mode = EditingMode.NONE

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
        elif self.__mode != EditingMode.NONE:

            #lewy przycisk myszki
            if self._command == Command.CLICKED_LMB:
            
                #tworzenie nowej platformy
                if self.__mode == EditingMode.PLATFORM_CREATION:
                    #TODO
                    #sprawdzenie czy nie nachodzi/koliduje z innymi obiektami
                    #albo i bez tego, gdyż wtedy można [łatwiej] robić platformy, które nie są prostokątami
            
                    if self.__newPlatformCoords == (-1, -1):
                        self.__newPlatformCoords = py.mouse.get_pos()
                    else:
                        #TODO
                        #dodanie nowej platformy o współrzędnych wierzchołków [tworzących przekątną] - (self.__newPlatformCoords, py.mouse.get_pos())
                        pass
            
                elif self.__mode == EditingMode.OBJECT_PLACEMENT:
                    #TODO
                    #sprawdzenie kolizji i dodanie do poziomu
                    pass
            
            #prawy przycisk myszki
            elif self._command == Command.CLICKED_RMP:

                #w trybie tworzenia platformy
                if self.__mode == EditingMode.PLATFORM_CREATION:

                    #ale bez wierzchołków - wychodzimy z tego trybu
                    if self.__newPlatformCoords == (-1, -1):
                        self.__mode = EditingMode.NONE

                    #już z jednym wierzchołkiem - usuwamy go
                    else:
                        self.__newPlatformCoords = (-1, -1)

                #w trybie wstawianie nowego obiektu
                elif self.__mode == EditingMode.OBJECT_PLACEMENT:
                    self.__mode == EditingMode.NONE
