from .model import Model
from src.enum.command import Command
from src.enum.editingMode import EditingMode
from src.view.Game.gameObject import GameObject
from src.enum.objectType import ObjectType
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

        #czy aktualnie jest przemieszczany obiekt
        self.__is_moved = False

        #aktualny tryb pracy
        self.__mode = EditingMode.NONE

        #tabela dla obiektów w grze
        self.__game_objects_arr = []

        self.__snap_distance = 10

    #metoda aktualizująca stan wewnętrzego modelu programu
    def update(self):
        
        if self._command == Command.EXIT:
            self._runMode = False

        elif self._command == Command.PREV_LEVEL and self.__level_to_edit > 0:
            self.__level_to_edit -= 1

        elif self._command == Command.NEXT_LEVEL and self.__level_to_edit < (len(self.__level_list) - 1):
            self.__level_to_edit += 1

        elif self._command == Command.EDIT and len(self.__level_list) > 0:
            self.__chosen_level = self.__level_to_edit
            #wczytanie nowego poziomu
            self.load_level_from_file()

        elif self._command == Command.CREATE_NEW:
            #utworzenie nowego poziomu
            pass

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

                    newVertexPos = (0, 0)
                    mouse_pos = py.mouse.get_pos()

                    for game_object in self.__game_objects_arr:
                            if game_object is GameObject and game_object.get_type() == ObjectType.STATIC:
                                x0 = game_object.get_x()
                                x1 = game_object.get_x() + game_object.get_width()
                                
                                y0 = game_object.get_y()
                                y1 = game_object.get_y() + game_object.get_height()

                                #jeżeli różnica między pozycją kursora myszki, a wierzchołkiem istniejącej platformy jest mniejsza niż ustalona
                                #wartość to nowy wierzchołek jest "przyczepiany" do już istniejącego
                                if abs(mouse_pos[0] - x0) < self.__snap_distance and abs(mouse_pos[1] - y0) < self.__snap_distance:
                                    newVertexPos = (x0, y0)
                                elif abs(mouse_pos[0] - x1) < self.__snap_distance and abs(mouse_pos[1] - y0) < self.__snap_distance:
                                    newVertexPos = (x1, y0)
                                elif abs(mouse_pos[0] - x0) < self.__snap_distance and abs(mouse_pos[1] - y1) < self.__snap_distance:
                                    newVertexPos = (x0, y1)
                                elif abs(mouse_pos[0] - x1) < self.__snap_distance and abs(mouse_pos[1] - y1) < self.__snap_distance:
                                    newVertexPos = (x1, y1)
                                else:
                                    newVertexPos = mouse_pos

                    if self.__new_platform_coords == (-1, -1):
                        self.__new_platform_coords = newVertexPos
                    else:
                        #dodanie nowej platformy o współrzędnych wierzchołków [tworzących przekątną] - (self.__newPlatformCoords, pozycja_kursora)
                        x0 = min(self.__newPlatformCoords[0], mouse_pos[0])
                        x1 = max(self.__newPlatformCoords[0], mouse_pos[0])

                        y0 = min(self.__newPlatformCoords[1], mouse_pos[1])
                        y1 = max(self.__newPlatformCoords[1], mouse_pos[1])

                        self.__game_objects_arr.append(GameObject(x0, y0, x1 - x0, y1 - y0, False, ObjectType.STATIC, None))
                        self.__new_platform_coords = (-1, -1)
            
                #elif self.__mode == EditingMode.OBJECT_PLACEMENT:
                    #TODO
                    #sprawdzenie kolizji i dodanie do poziomu
                    #pass

                #TODO
                #elif inne tryby jeszcze (bo była zmiana)
            
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

    def load_level_from_file(self):
        #odczyt wybranego przez użytkownika pliku
        
        #TODO
        #wczytanie poziomu (najlepiej jakby tu było wywołanie jednej metody klasy odpowiedzialnej za przechowywanie poziomu, ale czy tak będzie....)
        pass

    #v----GETTERY----v
    def get_level_to_edit_number(self):
        return self.__level_to_edit

    def get_new_platform_coords(self):
        return self.__new_platform_coords

    def get_mode(self):
        return self.__mode
