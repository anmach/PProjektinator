from .model import Model
from src.enum.command import Command
from src.enum.editingMode import EditingMode
from src.view.Game.gameObject import GameObject
from src.view.Game.dynamicObject import dynamicObject
from src.view.Game.player import Player
from src.view.Game.movingPlatform import MovingPlatform
from src.enum.objectType import ObjectType
from src.levelContainer import LevelContainer
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
        self.__chosen_level = 0

        #wyświetlany nr poziomu do edycji (zmieniany za pomocą przycisków)
        self.__level_to_edit = 0

        #współrzędne czegoś
        self.__something_coords = (-1, -1, -1, -1)

        #liczba ustalonych wierzchołków nowej platformy
        self.__new_platform_vertex_number = 1

        self.__moving_platform_placement_mode = 1

        #czy aktualnie jest przemieszczany obiekt
        self.__is_moved = False

        #aktualny tryb pracy
        self.__mode = EditingMode.NONE

        #tabela dla obiektów w grze
        self.__level = LevelContainer(define.get_levels_folder_path() + '\\' + self.__level_list[0], 0)
        self.__level.get_player().set_frame_by_id(1)

        #maksymalna odległość dla przyciągania wierzchołków
        self.__snap_distance = 10

        self.__is_player_placed = True

        self.__can_object_be_placed = True

        #przesuwanie poziomu
        self.__is_level_being_moved = False
        self.__prev_position = (0, 0)
        self.__translation = (0, 0)

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
            self.__level = LevelContainer(define.get_levels_folder_path() + '\\' + self.__level_list[self.__chosen_level], self.__chosen_level)
            if self.__level.get_player() != None:
                self.__level.get_player().set_frame_by_id(1)


        elif self._command == Command.CREATE_NEW:
            #utworzenie nowego poziomu
            pass

        elif self._command == Command.SAVE and self.__chosen_level != -1:
            #zapisanie aktualnie modyfikowanego poziomu
            self.__level.save_level_to_file()
            pass

        elif self._command == Command.CLICKED_MMB:
            #przesuwanie "kamery"
            if not self.__is_level_being_moved:
                self.__is_level_being_moved = True
                self.__prev_position = py.mouse.get_pos()
            else:
                new_position = py.mouse.get_pos()
                self.__translation = (new_position[0] - self.__prev_position[0], new_position[1] - self.__prev_position[1])
                self.__prev_position = new_position
                
            #przesunięcie wszystkich obiektów
            for game_object in self.__level.get_all_level_objects():
                game_object.set_pos(game_object.get_x() + self.__translation[0], game_object.get_y() + self.__translation[1])

        elif self._command == Command.DELETE_OBJECT:
            self.__mode = EditingMode.DELETION

            self.__something_coords = (-1, -1, -1, -1)
            self.__new_platform_vertex_number = 1

        elif self._command == Command.CREATE_PLATFORM:
            self.__mode = EditingMode.PLATFORM_CREATION

            self.__something_coords = (-1, -1, -1, -1)
            self.__new_platform_vertex_number = 1
        
        elif self._command == Command.PLACE_PLAYER:
            self.__mode = EditingMode.PLAYER_PLACEMENT

            self.__something_coords = (-1, -1, -1, -1)
            self.__new_platform_vertex_number = 1

        elif self._command == Command.PLACE_CRATE:
            self.__mode = EditingMode.CRATE_PLACEMENT

            self.__something_coords = (-1, -1, -1, -1)
            self.__new_platform_vertex_number = 1

        elif self._command == Command.PLACE_MOVING_PLATFORM:
            self.__mode = EditingMode.MOVING_PLATFORM_PLACEMENT

            self.__something_coords = (-1, -1, -1, -1)
            self.__new_platform_vertex_number = 1

        if self._command != Command.CLICKED_MMB:
            self.__is_level_being_moved = False
        #interpretacja akcji użytkownika na polu edycyjnym zależy od trybu w
        #jakim znajduje się edytor
            
        #tworzenie nowej platformy
        if self.__mode == EditingMode.PLATFORM_CREATION:
            self.update_platform_creation()

        #wstawianie nowego obiektu
        elif self.__mode == EditingMode.PLAYER_PLACEMENT:
            self.update_player_placement()
        
        #usuwanie obiektu (lub platformy)
        elif self.__mode == EditingMode.DELETION:
            self.update_deletion()

        elif self.__mode == EditingMode.CRATE_PLACEMENT:
            self.update_crate_placement()

        elif self.__mode == EditingMode.MOVING_PLATFORM_PLACEMENT:
            self.update_moving_platform_placement()

    def update_platform_creation(self):
        #TODO
        #sprawdzenie czy nie nachodzi/koliduje z innymi obiektami

        mouse_pos = py.mouse.get_pos()
        new_vertex_pos = mouse_pos
        if self.__new_platform_vertex_number == 1:
            #snap
            for game_object in self.__level.get_all_level_objects():
                    if game_object.get_type() == ObjectType.STATIC:
                        x0 = game_object.get_x()
                        x1 = game_object.get_x() + game_object.get_width()
                        
                        y0 = game_object.get_y()
                        y1 = game_object.get_y() + game_object.get_height()

                        #jeżeli różnica między pozycją kursora myszki, a
                        #wierzchołkiem istniejącej platformy jest mniejsza niż
                        #ustalona
                        #wartość to nowy wierzchołek jest "przyczepiany" do już
                        #istniejącego
                        if abs(mouse_pos[0] - x0) < self.__snap_distance and abs(mouse_pos[1] - y0) < self.__snap_distance:
                            new_vertex_pos = (x0, y0)
                        elif abs(mouse_pos[0] - x1) < self.__snap_distance and abs(mouse_pos[1] - y0) < self.__snap_distance:
                            new_vertex_pos = (x1, y0)
                        elif abs(mouse_pos[0] - x0) < self.__snap_distance and abs(mouse_pos[1] - y1) < self.__snap_distance:
                            new_vertex_pos = (x0, y1)
                        elif abs(mouse_pos[0] - x1) < self.__snap_distance and abs(mouse_pos[1] - y1) < self.__snap_distance:
                            new_vertex_pos = (x1, y1)

            self.__something_coords = (new_vertex_pos[0], new_vertex_pos[1], -1, -1)

        else:
            current_width = new_vertex_pos[0] - self.__something_coords[0]
            current_heigth = new_vertex_pos[1] - self.__something_coords[1]

            w_sign = 1 if current_width >= 0 else -1
            h_sign = 1 if current_heigth >= 0 else -1

            current_width = abs(current_width)
            current_heigth = abs(current_heigth)

            tile_width = define.get_platform_tile_standard_size()[0]
            tile_heigth = define.get_platform_tile_standard_size()[1]

            #min. 3-krotność wymiaru tekstury
            if current_width < 3 * tile_width + tile_width // 2:
                current_width = 3 * tile_width
            else:
                current_width -= 3 * tile_width
                sum = 3 * tile_width
                while current_width > tile_width:
                    current_width -= tile_width
                    sum += tile_width
                perc = float(current_width) / float(tile_width)
                if perc < 0.5:
                    current_width = sum
                else:
                    current_width = sum + tile_width

            #min. 3-krotność wymiaru tekstury
            if current_heigth < 3 * tile_heigth + tile_heigth // 2:
                current_heigth = 3 * tile_heigth
            else:
                current_heigth -= 3 * tile_heigth
                sum = 3 * tile_heigth
                while current_heigth > tile_heigth:
                    current_heigth -= tile_heigth
                    sum += tile_heigth
                perc = float(current_heigth) / float(tile_heigth)
                if perc < 0.5:
                    current_heigth = sum
                else:
                    current_heigth = sum + tile_heigth

            self.__something_coords = (self.__something_coords[0], self.__something_coords[1], self.__something_coords[0] + current_width * w_sign, self.__something_coords[1] + current_heigth * h_sign)

        if self._command == Command.CLICKED_LMB:
            if self.__new_platform_vertex_number == 1:
                self.__new_platform_vertex_number = 2
            else:
                #dodanie nowej platformy
                x0 = min(self.__something_coords[0], self.__something_coords[2])
                x1 = max(self.__something_coords[0], self.__something_coords[2])

                y0 = min(self.__something_coords[1], self.__something_coords[3])
                y1 = max(self.__something_coords[1], self.__something_coords[3])

                #new_object = GameObject(x0, y0, x1 - x0, y1 - y0, ObjectType.STATIC, None)

                self.__level.try_add_new_object(ObjectType.STATIC, x0, y0, x1 - x0, y1 - y0, ObjectType.STATIC)

                self.__something_coords = (-1, -1, -1, -1)
                self.__new_platform_vertex_number = 1

        if self._command == Command.CLICKED_RMB:

            if self.__new_platform_vertex_number == 1:
                self.__something_coords = (-1, -1, -1, -1)
                self.__mode = EditingMode.NONE
            else:
                self.__something_coords = (self.__something_coords[0], self.__something_coords[1], -1, -1)
                self.__new_platform_vertex_number = 1

    def update_player_placement(self):
        #sprawdzenie kolizji - TODO??  ulepszenie tego?  żeby nie sprawdzać z
        #każdym obiektem
        mouse_pos = py.mouse.get_pos()
        
        #nowa pozycja gracza - TODO - zmienić dla zmian rozdzielczości
        x0 = mouse_pos[0] - int(0.5 * define.get_player_standard_size()[0])
        x1 = x0 + define.get_player_standard_size()[0]

        y0 = mouse_pos[1] - int(0.5 * define.get_player_standard_size()[1])
        y1 = y0 + define.get_player_standard_size()[1]

        self.__something_coords = (x0, y0, x1, y1)

        self.__can_object_be_placed = True

        #sprawdzenie "kolizji"
        for obj in self.__level.get_all_level_objects():
            if self.is_colliding((obj.get_x(), obj.get_x() + obj.get_width(), obj.get_y(), obj.get_y() + obj.get_height()), (x0, x1, y0, y1)):
                self.__can_object_be_placed = False
                break

        if self._command == Command.CLICKED_LMB and not self.__is_player_placed and self.__can_object_be_placed:
            #stworzenie gracza
            self.__level.try_add_new_object(ObjectType.PLAYER, x0, y0, define.get_player_standard_size()[0], define.get_player_standard_size()[1], ObjectType.PLAYER)
            self.__level.get_player().set_frame_by_id(1)
            
            #zapamiętanie, że gracz już został dodany
            self.__is_player_placed = True

            self.__something_coords = (-1, -1, -1, -1)

            #po dodaniu zmień tryb
            self.__mode = EditingMode.NONE

        elif self._command == Command.CLICKED_RMB:
            self.__something_coords = (-1, -1, -1, -1)
            self.__mode = EditingMode.NONE

    def update_crate_placement(self):
         mouse_pos = py.mouse.get_pos()
         new_vertex_pos = mouse_pos
         
         if self.__new_platform_vertex_number == 1:
             self.__something_coords = (new_vertex_pos[0], new_vertex_pos[1], -1, -1)
         else:
             self.__something_coords = (self.__something_coords[0], self.__something_coords[1], new_vertex_pos[0], new_vertex_pos[1])
         
         if self._command == Command.CLICKED_LMB:
             if self.__new_platform_vertex_number == 1:
                 self.__new_platform_vertex_number = 2
             else:
                 #dodanie nowej platformy
                 x0 = min(self.__something_coords[0], self.__something_coords[2])
                 x1 = max(self.__something_coords[0], self.__something_coords[2])
         
                 y0 = min(self.__something_coords[1], self.__something_coords[3])
                 y1 = max(self.__something_coords[1], self.__something_coords[3])
         
                 #new_object = dynamicObject(x0, y0, x1 - x0, y1 - y0, True, ObjectType.DYNAMIC, None)
         
                 #self.__game_objects_arr.append(new_object)
                 #self.__all_sprites.add(new_object)
            
                 self.__level.try_add_new_object(ObjectType.DYNAMIC, x0, y0, x1 - x0, y1 - y0, ObjectType.DYNAMIC)

                 self.__something_coords = (-1, -1, -1, -1)
                 self.__new_platform_vertex_number = 1

         elif self._command == Command.CLICKED_RMB:
         
             if self.__new_platform_vertex_number == 1:
                 self.__something_coords = (-1, -1, -1, -1)
                 self.__mode = EditingMode.NONE
             else:
                 self.__something_coords = (self.__something_coords[0], self.__something_coords[1], -1, -1)
                 self.__new_platform_vertex_number = 1

    def update_moving_platform_placement(self):
        mouse_pos = py.mouse.get_pos()

        if self.__moving_platform_placement_mode == 1:
            new_vertex_pos = mouse_pos

            if self.__new_platform_vertex_number == 1:
                self.__something_coords = (new_vertex_pos[0], new_vertex_pos[1], -1, -1, -1, -1)
            else:
                self.__something_coords = (self.__something_coords[0], self.__something_coords[1], new_vertex_pos[0], new_vertex_pos[1], -1, -1)
            
            if self._command == Command.CLICKED_LMB:
                if self.__new_platform_vertex_number == 1:
                    self.__new_platform_vertex_number = 2
                else:
                    self.__moving_platform_placement_mode = 2

            elif self._command == Command.CLICKED_RMB:
            
                if self.__new_platform_vertex_number == 1:
                    self.__something_coords = (-1, -1, -1, -1)
                    self.__mode = EditingMode.NONE
                else:
                    self.__something_coords = (self.__something_coords[0], self.__something_coords[1], -1, -1, -1, -1)
                    self.__new_platform_vertex_number = 1

        elif self.__moving_platform_placement_mode == 2:
            #TODO sprawdzanie kolizji

            #współrzędne środka ustalonej już początkowej pozycji platofrmy
            centre = (int(0.5 * (self.__something_coords[0] + self.__something_coords[2])),  int(0.5 * (self.__something_coords[1] + self.__something_coords[3])))
            
            #różnica pozycji (współrzędne środków)
            pos_diffr = (mouse_pos[0] - centre[0], mouse_pos[1] - centre[1])

            #współrzędne pozycji początkowej (x1, y1, x2, y2) oraz różnica pozycji (dx, dy)
            self.__something_coords = (self.__something_coords[0], self.__something_coords[1], self.__something_coords[2], self.__something_coords[3], pos_diffr[0], pos_diffr[1])

            if self._command == Command.CLICKED_LMB:
                #dodanie nowej poruszającej się platformy
                x0 = min(self.__something_coords[0], self.__something_coords[2])
                x1 = max(self.__something_coords[0], self.__something_coords[2])

                y0 = min(self.__something_coords[1], self.__something_coords[3])
                y1 = max(self.__something_coords[1], self.__something_coords[3])

                #new_object = MovingPlatform(x0, y0, x1 - x0, y1 - y0, False, ObjectType.KINEMATIC, None, self.__something_coords[4], self.__something_coords[5], 2, 2)
                #self.__game_objects_arr.append(new_object)
                #self.__all_sprites.add(new_object)

                self.__level.try_add_new_object(ObjectType.KINEMATIC, x0, y0, x1 - x0, y1 - y0, ObjectType.KINEMATIC, 2, 2, self.__something_coords[4], self.__something_coords[5])

                self.__new_platform_vertex_number = 1
                self.__moving_platform_placement_mode = 1
                self.__something_coords = (-1, -1, -1, -1)
                self.__mode = EditingMode.NONE


            elif self._command == Command.CLICKED_RMB:
                self.__moving_platform_placement_mode = 1

    def update_deletion(self):
        obj_to_del = None
        self.__something_coords = (-1, -1, -1, -1)

        mouse_pos = py.mouse.get_pos()

        #wyszukiwanie obietku nad którym znajduje się kursor myszy (potenjalny
        #kandydat do usunięcia)
        for object in self.__level.get_all_level_objects():
            if object.get_x() <= mouse_pos[0] and object.get_x() + object.get_width() >= mouse_pos[0] and object.get_y() <= mouse_pos[1] and object.get_y() + object.get_height() >= mouse_pos[1]:
                
                #pobranie jego wymiarów (wsp.  x, y oraz szerokość i wysokość)
                self.__something_coords = (object.get_x(), object.get_y(), object.get_x() + object.get_width(), object.get_y() + object.get_height())
                
                #zapamiętanie jego indeksu
                obj_to_del = object
                break

        if self._command == Command.CLICKED_LMB and len(self.__level.get_all_level_objects()) > 0:
            #deleted_object = self.__level.get_all_level_objects().pop(obj_to_del_index)
            #self.__level.get_sprite_group().remove(deleted_object)
            self.__level.try_delete_object(obj_to_del)

            #jeśli był to gracz to zapamiętaj, że już go nie
            if isinstance(object, Player):
                self.__is_player_placed = False

            self.__something_coords = (-1, -1, -1, -1)

    def load_level_from_file(self):
        #odczyt wybranego przez użytkownika pliku
        
        #TODO
        #wczytanie poziomu (najlepiej jakby tu było wywołanie jednej metody
        #klasy odpowiedzialnej za przechowywanie poziomu, ale czy tak
        #będzie....)
        pass

    def is_colliding(self, first = (0, 0, 0, 0), second = (0, 0, 0, 0)):
        """ funkcja zwraca True jeśli obiekty nachodzą na siebie
        first oraz second zawierają współrzędne w kolejności: x_lewy, x_prawy, y_gorny, y_dolny"""

        first_size_from_centre = ((first[1] - first[0]) / 2.0, (first[3] - first[2]) / 2.0)
        second_size_from_centre = ((second[1] - second[0]) / 2.0, (second[3] - second[2]) / 2.0)

        first_centre = (first[1] - first_size_from_centre[0], first[3] - first_size_from_centre[1])
        second_centre = (second[1] - second_size_from_centre[0], second[3] - second_size_from_centre[1])
        
        if abs(second_centre[0] - first_centre[0]) <= first_size_from_centre[0] + second_size_from_centre[0]  and abs(second_centre[1] - first_centre[1]) <= first_size_from_centre[1] + second_size_from_centre[1]:
            return True
        return False

    #v----GETTERY----v
    def get_level_to_edit_number(self):
        return self.__level_to_edit

    def get_mode(self):
        return self.__mode

    def get_all_sprites(self):
        return self.__level.get_sprite_group()

    def get_level(self):
        return self.__level

    def get_something_coords(self):
        return self.__something_coords

    def get_translation(self):
        return self.__translation

    def get_can_object_be_placed(self):
        return self.__can_object_be_placed
