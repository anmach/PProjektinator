from .model import Model
from src.enum.command import Command
from src.enum.editingMode import EditingMode
from src.view.Game.gameObject import GameObject
from src.view.Game.player import Player
from src.enum.objectType import ObjectType
import os
import pygame as py
import src.define as define


class ModelLevelEditor(Model):

    def __init__(self):
        super().__init__()

        #pobranie informacji o utworzonych już poziomach
        #       v-----inaczej nie działa-----v
        for (_, _, file_list) in os.walk(define.get_levels_folder_path()):
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

        self.__object_to_delete_coords = (-1, -1, -1, -1)

        self.__is_player_placed = False

        self.__can_object_be_placed = True

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

        elif self._command == Command.DELETE_OBJECT:
            self.__mode = EditingMode.DELETION

            self.__new_platform_first_vertex_pos = (-1, -1)
            self.__new_platform_second_vertex_pos = (-1, -1)
            self.__new_platform_vertex_number = 1

        elif self._command == Command.CREATE_PLATFORM:
            self.__mode = EditingMode.PLATFORM_CREATION

            self.__new_platform_first_vertex_pos = (-1, -1)
            self.__new_platform_second_vertex_pos = (-1, -1)
            self.__new_platform_vertex_number = 1
        
        elif self._command == Command.PLACE_PLAYER:
            self.__mode = EditingMode.PLAYER_PLACEMENT

            self.__new_platform_first_vertex_pos = (-1, -1)
            self.__new_platform_second_vertex_pos = (-1, -1)
            self.__new_platform_vertex_number = 1

        #interpretacja akcji użytkownika na polu edycyjnym zależy od trybu w jakim znajduje się edytor
            
        #tworzenie nowej platformy
        if self.__mode == EditingMode.PLATFORM_CREATION:
            self.update_platform_creation()

        #wstawianie nowego obiektu
        elif self.__mode == EditingMode.PLAYER_PLACEMENT:
            self.update_player_placement()
        
        #usuwanie obiektu (lub platformy)
        elif self.__mode == EditingMode.DELETION:
            self.update_deletion()

    def update_platform_creation(self):
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

    def update_player_placement(self):
        #sprawdzenie kolizji - TODO?? ulepszenie tego? żeby nie sprawdzać z każdym obiektem
        mouse_pos = py.mouse.get_pos()
        
        #nowa pozycja gracza - TODO - zmienić dla zmian rozdzielczości
        x0 = mouse_pos[0] - int(0.5 * define.get_player_standard_size()[0])
        x1 = x0 + define.get_player_standard_size()[0]

        y0 = mouse_pos[1] - int(0.5 * define.get_player_standard_size()[1])
        y1 = y0 + define.get_player_standard_size()[1]

        self.__can_object_be_placed = True

        for obj in self.__game_objects_arr:
            if self.is_colliding((obj.get_x(), obj.get_x() + obj.get_width(), obj.get_y(), obj.get_y() + obj.get_height()), (x0, x1, y0, y1)):
                self.__can_object_be_placed = False
                break

        if self._command == Command.CLICKED_LMB and not self.__is_player_placed and self.__can_object_be_placed:
            #stworzenie gracza
            new_object = Player(define.get_player_sprites_folder_path())
            new_object.set_pos(x0, y0)
            new_object.set_frame_by_id(1)

            #dodanie go do tablicy obiektów i sprajtów
            self.__game_objects_arr.append(new_object)
            self.__all_sprites.add(new_object)

            #zapamiętanie, że gracz już został dodany
            self.__is_player_placed = True

            #po dodaniu zmień tryb
            self.__mode = EditingMode.NONE

    def update_deletion(self):
        obj_to_del_index = -1
        self.__object_to_delete_coords = (-1, -1, -1, -1)

        mouse_pos = py.mouse.get_pos()

        #wyszukiwanie obietku nad którym znajduje się kursor myszy (potenjalny kandydat do usunięcia)
        for object in self.__game_objects_arr:
            if object.get_x() <= mouse_pos[0] and object.get_x() + object.get_width() >= mouse_pos[0] and object.get_y() <= mouse_pos[1] and object.get_y() + object.get_height() >= mouse_pos[1]:
                
                #pobranie jego wymiarów (wsp. x, y oraz szerokość i wysokość)
                self.__object_to_delete_coords = (object.get_x(), object.get_y(), object.get_width(), object.get_height())
                
                #zapamiętanie jego indeksu
                obj_to_del_index = self.__game_objects_arr.index(object)
                break

        if self._command == Command.CLICKED_LMB and len(self.__game_objects_arr) > 0 and obj_to_del_index != -1:
            deleted_object = self.__game_objects_arr.pop(obj_to_del_index)
            self.__all_sprites.remove(deleted_object)

            #jeśli był to gracz to zapamiętaj, że już go nie
            if isinstance(deleted_object, Player):
                self.__is_player_placed = False

    def load_level_from_file(self):
        #odczyt wybranego przez użytkownika pliku
        
        #TODO
        #wczytanie poziomu (najlepiej jakby tu było wywołanie jednej metody klasy odpowiedzialnej za przechowywanie poziomu, ale czy tak będzie....)
        pass

    def is_colliding(self, first = (0, 0, 0, 0), second = (0, 0, 0, 0)):
        """ funkcja zwraca True jeśli obiekty nachodzą na siebie (nawet dla "wspólnego" wierzchołka czu boku
        first oraz second zawierają współrzędne w kolejności: x_lewy, x_prawy, y_gorny, y_dolny"""

        if first[0] >= second[0] and first[0] <= second[1] and first[2] >= second[2] and first[2] <= second[3] \
        or first[1] >= second[0] and first[1] <= second[1] and first[2] >= second[2] and first[2] <= second[3] \
        or first[0] >= second[0] and first[0] <= second[1] and first[3] >= second[2] and first[3] <= second[3] \
        or first[1] >= second[0] and first[1] <= second[1] and first[3] >= second[2] and first[3] <= second[3]:
            return True
        return False

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

    def get_obj_to_del_coords(self):
        return self.__object_to_delete_coords
