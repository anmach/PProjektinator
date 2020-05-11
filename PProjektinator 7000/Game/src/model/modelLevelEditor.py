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
        self.__new_platform_first_vertex_pos = (-1, -1)
        self.__new_platform_second_vertex_pos = (-1, -1)
        self.__new_platform_vertex_number = 1

        #czy aktualnie jest przemieszczany obiekt
        self.__is_moved = False

        #aktualny tryb pracy
        self.__mode = EditingMode.NONE

        #tabela dla obiektów w grze
        self.__game_objects_arr = []

        #maksymalna odległość dla przyciągania wierzchołków
        self.__snap_distance = 10

        self.__all_sprites = py.sprite.Group()

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
            #zapisanie aktualnie modyfikowanego poziomu
            pass

        elif self._command == Command.CREATE_PLATFORM:
            self.__mode = EditingMode.PLATFORM_CREATION
        
        elif self._command == Command.PLACE_PLAYER:
            self.__mode = EditingMode.OBJECT_PLACEMENT

        #interpretacja akcji użytkownika zależy od trybu w znajduje się edytor
            
        #tworzenie nowej platformy
        if self.__mode == EditingMode.PLATFORM_CREATION:
            #TODO
            #sprawdzenie czy nie nachodzi/koliduje z innymi obiektami

            mouse_pos = py.mouse.get_pos()
            new_vertex_pos = mouse_pos

            for game_object in self.__game_objects_arr:
                    if type(game_object) is GameObject and game_object.get_type() == ObjectType.STATIC:
                        x0 = game_object.get_x()
                        x1 = game_object.get_x() + game_object.get_width()
                        
                        y0 = game_object.get_y()
                        y1 = game_object.get_y() + game_object.get_height()

                        #jeżeli różnica między pozycją kursora myszki, a wierzchołkiem istniejącej platformy jest mniejsza niż ustalona
                        #wartość to nowy wierzchołek jest "przyczepiany" do już istniejącego
                        if abs(mouse_pos[0] - x0) < self.__snap_distance and abs(mouse_pos[1] - y0) < self.__snap_distance:
                            new_vertex_pos = (x0, y0)
                        elif abs(mouse_pos[0] - x1) < self.__snap_distance and abs(mouse_pos[1] - y0) < self.__snap_distance:
                            new_vertex_pos = (x1, y0)
                        elif abs(mouse_pos[0] - x0) < self.__snap_distance and abs(mouse_pos[1] - y1) < self.__snap_distance:
                            new_vertex_pos = (x0, y1)
                        elif abs(mouse_pos[0] - x1) < self.__snap_distance and abs(mouse_pos[1] - y1) < self.__snap_distance:
                            new_vertex_pos = (x1, y1)

            if self.__new_platform_vertex_number == 1:
                self.__new_platform_first_vertex_pos = new_vertex_pos
            else:
                self.__new_platform_second_vertex_pos = new_vertex_pos

            if self._command == Command.CLICKED_LMB:
                if self.__new_platform_vertex_number == 1:
                    self.__new_platform_vertex_number = 2
                else:
                    #dodanie nowej platformy
                    x0 = min(self.__new_platform_first_vertex_pos[0], self.__new_platform_second_vertex_pos[0])
                    x1 = max(self.__new_platform_first_vertex_pos[0], self.__new_platform_second_vertex_pos[0])
                                                                      
                    y0 = min(self.__new_platform_first_vertex_pos[1], self.__new_platform_second_vertex_pos[1])
                    y1 = max(self.__new_platform_first_vertex_pos[1], self.__new_platform_second_vertex_pos[1])

                    new_object = GameObject(x0, y0, x1 - x0, y1 - y0, False, ObjectType.STATIC, None)

                    self.__game_objects_arr.append(new_object)
                    self.__all_sprites.add(new_object)

                    self.__new_platform_first_vertex_pos = self.__new_platform_second_vertex_pos = (-1, -1)
                    self.__new_platform_vertex_number = 1
            if self._command == Command.CLICKED_RMB:

                if self.__new_platform_vertex_number == 1:
                    self.__new_platform_first_vertex_pos = (-1, -1)
                    self.__mode = EditingMode.NONE
                else:
                    self.__new_platform_second_vertex_pos = (-1, -1)
                    self.__new_platform_vertex_number = 1

        elif self.__mode == EditingMode.OBJECT_PLACEMENT:
            #TODO zrobić to
            pass
        

    def load_level_from_file(self):
        #odczyt wybranego przez użytkownika pliku
        
        #TODO
        #wczytanie poziomu (najlepiej jakby tu było wywołanie jednej metody klasy odpowiedzialnej za przechowywanie poziomu, ale czy tak będzie....)
        pass

    #v----GETTERY----v
    def get_level_to_edit_number(self):
        return self.__level_to_edit

    def get_new_platform_first_vertex_pos(self):
        return self.__new_platform_first_vertex_pos

    def get_new_platform_second_vertex_pos(self):
        return self.__new_platform_second_vertex_pos

    def get_mode(self):
        return self.__mode

    def get_all_sprites(self):
        return self.__all_sprites
