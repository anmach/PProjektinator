import pygame as py
from src.enum.objectType import ObjectType
from src.view.Game.gameObject import GameObject
from src.view.Game.movingObject import MovingObject
from src.view.Game.dynamicObject import dynamicObject
from src.view.Game.player import Player
import src.define as define

class LevelContainer(object):
    """Klasa przechowująca informacje o obiektach znajdujących się w grze"""

    def __init__(self, level_file_name, level_number):
        self._level_file_name = level_file_name
        self._level_number = level_number

        # Aktualne rozmiary okna
        self._surface_width = -1
        self._surface_height = -1
        # Rozmiary okna według obiektów w kontenerze
        self._objects_base_width = -1
        self._objects_base_height = -1

        self._mini_platforms = []
        self._platforms = []
        self._moving_platforms = []
        self._crates = []

        self._enemies = []
        self._finish_lines = []
        self._player = None

        # poziom odczytany bez odkrytych błędów, ale może nie mieć playera
        self._level_read_without_errors = 0

        # poziom odczytany bez błędów, z graczem
        self._level_read_success = self.try_load_level_from_file()

    def try_load_level_from_file(self):          
        self._level_read_without_errors = 0
        file = open(self._level_file_name, 'r')

        # Którą z kolei linię danych o obiekcie czytamy
        line_of_object_info = 0

        # Jakie info po kolei zbieramy o obiekcie
        id = -1
        x = -1
        y = -1
        width = -1
        height = -1                
        # Dodatkowe info - KINEMATIC
        movement_max_x = -1
        movement_max_y = -1
        speed_x = -1
        speed_y = -1
                
        # Odczyt kolejnych linii
        for line in file:
            # Usunięcie znaków białych
            splitted_line = line.strip().split()    

            if splitted_line[0] == "@":
                if line_of_object_info != 0:
                    if self.try_add_new_object(id, x, y, width, height, type, speed_x, speed_y, movement_max_x, movement_max_y) == 0:
                        # Nie udało się dodać obiektu
                        return 0
                                   
                # Reset danych
                line_of_object_info = 0                
                id = -1
                x = -1
                y = -1
                width = -1
                height = -1                
                movement_max_x = -1
                movement_max_y = -1
                speed_x = -1
                speed_y = -1

            elif splitted_line[0] == "$":
                if self.try_add_new_object(id, x, y, width, height, type, speed_x, speed_y, movement_max_x, movement_max_y) == 0:
                    # Nie udało się dodać obiektu
                    return 0

            elif splitted_line[0] == "%":
                self._objects_base_width = int(splitted_line[1])
                self._objects_base_height = int(splitted_line[2])

            elif splitted_line[0] == "#":
                pass

            elif line_of_object_info == 0:
                id = int(splitted_line[0])
                line_of_object_info += 1

            elif line_of_object_info == 1:
                x = int(splitted_line[0])
                line_of_object_info += 1 

            elif line_of_object_info == 2:
                y = int(splitted_line[0])
                line_of_object_info += 1
                
            elif line_of_object_info == 3:
                width = int(splitted_line[0])
                line_of_object_info += 1
                
            elif line_of_object_info == 4:
                height = int(splitted_line[0])
                line_of_object_info += 1
                
            elif line_of_object_info == 5:
                movement_max_x = int(splitted_line[0])
                line_of_object_info += 1
                
            elif line_of_object_info == 6:
                movement_max_y = int(splitted_line[0])
                line_of_object_info += 1
                
            elif line_of_object_info == 7:
                speed_x = int(splitted_line[0])
                line_of_object_info += 1
                
            elif line_of_object_info == 8:
                speed_y = int(splitted_line[0])
                line_of_object_info += 1

            else:
                # Błąd odczytu, za dużo linii
                return 0

        file.close()
        
        self._level_read_without_errors = 1
        self._mini_platforms = self.create_mini_platforms()

        if self._player:
            # Udało się odczytać plik poprawnie (chyba)
            return 1
        else:
            # Nie ma gracza
            return 0

    def try_add_new_object(self, id, x, y, width, height, type, speed_x=-1, speed_y=-1, movement_max_x=-1, movement_max_y=-1):
        if id < 0 or x < 0 or y < 0 or width <= 0 or height <= 0:
            # Błąd - niepoprawne dane
            return 0
        # Dodawanie obiektu
        if id == ObjectType.STATIC:
            self._platforms.append(GameObject(x, y, width, height, ObjectType.STATIC, None))            
        elif id == ObjectType.DYNAMIC:
            self._crates.append(dynamicObject(x, y, width, height, True, ObjectType.DYNAMIC, None))
        elif id == ObjectType.FINISH_LINE:
            self._finish_lines.append(GameObject(x, y, width, height, ObjectType.FINISH_LINE, define.get_end_game_sprites_folder_path()))
        elif id == ObjectType.KINEMATIC:
            if speed_x < 0 or speed_y < 0:# or movement_max_x < 0 or movement_max_y < 0:
                # Błąd - niepoprawne dane
                return 0
            self._moving_platforms.append(MovingObject(x,y, width, height, False, ObjectType.KINEMATIC, None, movement_max_x, movement_max_y, speed_x, speed_y))
        elif id == ObjectType.PLAYER:
            self._player = Player(x, y, width, height, True, ObjectType.PLAYER, define.get_player_sprites_folder_path())
        elif id == ObjectType.ENEMY:
            if speed_x < 0 or speed_y < 0:# or movement_max_x < 0 or movement_max_y < 0:
                # Błąd - niepoprawne dane
                return 0
            self._enemies.append(MovingObject(x,y, width, height, False, ObjectType.ENEMY, None, movement_max_x, movement_max_y, speed_x, speed_y))
        else:
            # Błąd - nieznany typ
            return 0

    def try_delete_object(self, object):
        index = 0
        for item in self._platforms:
            if item == object:
                self._platforms.pop(index)
                return
            else:
                index += 1

        index = 0
        for item in self._crates:
            if item == object:
                self._crates.pop(index)
                return
            else:
                index += 1

        index = 0
        for item in self._moving_platforms:
            if item == object:
                self._moving_platforms.pop(index)
                return
            else:
                index += 1

        index = 0
        for item in self._enemies:
            if item == object:
                self._enemies.pop(index)
                return
            else:
                index += 1

        index = 0
        for item in self._finish_lines:
            if item == object:
                self._finish_lines.pop(index)
                return
            else:
                index += 1

        if object == self._player:
            self._player = None

    def save_level_to_file(self):        
        file = open(self._level_file_name, 'w')
        file.truncate(0)

        if self._player != None:            
            file.write('@')        
            file.write('\n')      
            file.write(str(int(ObjectType.PLAYER))) #id
            file.write('\n')          
            file.write(str(self._player.get_x())) # x
            file.write('\n')        
            file.write(str(self._player.get_y())) # y
            file.write('\n')          
            file.write(str(self._player.get_width())) # szerokość
            file.write('\n')          
            file.write(str(self._player.get_height())) # wysokość
            file.write('\n')  

        for platform in self._platforms:        
            file.write('@')   
            file.write('\n')           
            file.write(str(int(ObjectType.STATIC))) # id
            file.write('\n')          
            file.write(str(platform.get_x())) # x
            file.write('\n')        
            file.write(str(platform.get_y())) # y
            file.write('\n')          
            file.write(str(platform.get_width())) # szerokość
            file.write('\n')          
            file.write(str(platform.get_height())) # wysokość
            file.write('\n')  

        for crate in self._crates:        
            file.write('@') 
            file.write('\n')             
            file.write(str(int(ObjectType.DYNAMIC))) # id
            file.write('\n')          
            file.write(str(crate.get_x())) # x
            file.write('\n')        
            file.write(str(crate.get_y())) # y
            file.write('\n')          
            file.write(str(crate.get_width())) # szerokość
            file.write('\n')          
            file.write(str(crate.get_height())) # wysokość
            file.write('\n')  

        for mov_plat in self._moving_platforms:        
            file.write('@')   
            file.write('\n')           
            file.write(str(int(ObjectType.KINEMATIC))) # id
            file.write('\n')          
            file.write(str(mov_plat.get_x())) # x
            file.write('\n')        
            file.write(str(mov_plat.get_y())) # y
            file.write('\n')          
            file.write(str(mov_plat.get_width())) # szerokość
            file.write('\n')          
            file.write(str(mov_plat.get_height())) # wysokość
            file.write('\n')          
            file.write(str(mov_plat.get_path_max_x())) # max x
            file.write('\n')          
            file.write(str(mov_plat.get_path_max_y())) # max y
            file.write('\n')          
            file.write(str(mov_plat.get_spd_x())) # speed x
            file.write('\n')          
            file.write(str(mov_plat.get_spd_y())) # speed y
            file.write('\n')

        for enemy in self._enemies:        
            file.write('@')   
            file.write('\n')           
            file.write(str(int(ObjectType.ENEMY))) # id
            file.write('\n')       
            file.write(str(enemy.get_x())) # x
            file.write('\n')        
            file.write(str(enemy.get_y())) # y
            file.write('\n')          
            file.write(str(enemy.get_width())) # szerokość
            file.write('\n')          
            file.write(str(enemy.get_height())) # wysokość
            file.write('\n')          
            file.write(str(enemy.get_path_max_x())) # max x
            file.write('\n')          
            file.write(str(enemy.get_path_max_y())) # max y
            file.write('\n')          
            file.write(str(enemy.get_spd_x())) # speed x
            file.write('\n')          
            file.write(str(enemy.get_spd_y())) # speed y
            file.write('\n')
           
        for line in self._finish_lines:       
            file.write('@')   
            file.write('\n')           
            file.write(str(int(ObjectType.FINISH_LINE))) # id
            file.write('\n')          
            file.write(str(platform.get_x())) # x
            file.write('\n')        
            file.write(str(platform.get_y())) # y
            file.write('\n')          
            file.write(str(platform.get_width())) # szerokość
            file.write('\n')          
            file.write(str(platform.get_height())) # wysokość
            file.write('\n')  

        file.write('$')
        file.close()

    def delete_all_objects(self):
        self._player = None
        self._crates.clear()
        self._platforms.clear()
        self._moving_platforms.clear()
        self._enemies.clear()
        self._finish_lines.clear()

    def resize_objects_for_surface_size(self):
        if self._objects_base_height != -1 and self._objects_base_width != -1 and self._surface_height != -1 and self._surface_width != 1:
            for mov_pla in self._moving_platforms:
                mov_pla.set_heigth(int(self._surface_height * mov_pla.get_height() / self._objects_base_height))
                mov_pla.set_pos(mov_pla.get_x(), int(self._surface_height * mov_pla.get_y() / self._objects_base_height))

            for platform in self._platforms:
                platform.set_heigth(int(self._surface_height * platform.get_height() / self._objects_base_height))
                platform.set_pos(platform.get_x(), int(self._surface_height * platform.get_y() / self._objects_base_height))

            if self._player != None:
                self._player.set_heigth(int(self._surface_height * self._player.get_height() / self._objects_base_height))
                self._player.set_pos(self._player.get_x(), int(self._surface_height * self._player.get_y() / self._objects_base_height))

            for crate in self._crates:
                crate.set_heigth(int(self._surface_height * crate.get_height() / self._objects_base_height))
                crate.set_pos(crate.get_x(), int(self._surface_height * crate.get_y() / self._objects_base_height))

            for enemy in self._enemies:
                enemy.set_heigth(int(self._surface_height * enemy.get_height() / self._objects_base_height))
                enemy.set_pos(enemy.get_x(), int(self._surface_height * enemy.get_y() / self._objects_base_height))

            for line in self._finish_lines:
                line.set_heigth(int(self._surface_height * line.get_height() / self._objects_base_height))
                line.set_pos(line.get_x(), int(self._surface_height * line.get_y() / self._objects_base_height))

    # Gettery
    def get_level_file_name(self):
        return self._level_file_name

    def get_level_read_succes(self):
        return self._level_read_success

    def get_level_read_without_errors(self):
        return self._read_level_without_errors

    def get_all_level_objects(self):
        objects = []

        for item in self._platforms:
            objects.append(item)

        for item in self._crates:
            objects.append(item)

        for item in self._moving_platforms:
            objects.append(item)

        for item in self._enemies:
            objects.append(item)

        for item in self._finish_lines:
            objects.append(item)

        if self._player != None:
            objects.append(self._player)

        return objects

    def get_platforms(self):
        return self._platforms

    def get_crates(self):
        return self._crates

    def get_moving_platforms(self):
        return self._moving_platforms

    def get_enemies(self):
        return self._enemies

    def get_finish_lines(self):
        return self._finish_lines

    def get_player(self):
        return self._player

    def get_sprite_group(self):
        group = py.sprite.Group()

        for item in self._moving_platforms:
            group.add(item)

        for platform in self._mini_platforms:
            group.add(platform)

        if self._player != None:
            group.add(self._player)

        for crate in self._crates:
            group.add(crate)

        for enemy in self._enemies:
            group.add(enemy)

        for line in self._finish_lines:
            group.add(line)

        return group

    def create_mini_platforms(self):
        mini_platforms = []

        #podział na mniejsze platformy

        tile_size = define.get_platform_tile_standard_size()

        for plat in self._platforms:
            x = plat.get_x()
            y = plat.get_y()
            height = plat.get_height()
            width = plat.get_width()
            
            columns_count = width // define.get_platform_tile_standard_size()[0]
            rows_count = height // define.get_platform_tile_standard_size()[1]

            tile = 0
            for i in range(0, columns_count):
                for j in range(0, rows_count):
                    if i == 0:
                        if j == 0:
                            tile = 2
                        elif j == rows_count - 1:
                            tile = 0
                        else:
                            tile = 5
                    elif i == columns_count - 1:
                        if j == 0:
                            tile = 3
                        elif j == rows_count - 1:
                            tile = 1
                        else:
                            tile = 7
                    else:
                        if j == 0:
                            tile = 8
                        elif j == rows_count - 1:
                            tile = 6
                        else:
                            tile = 4
                    mini_platforms.append(GameObject(x + i * tile_size[0], y + j * tile_size[1], tile_size[0], tile_size[1], ObjectType.STATIC, define.get_platform_sprites_folder_path()))
                    mini_platforms[-1].set_frame_by_id(tile)

        return mini_platforms

    # Marna nazwa
    # Zwraca grupę obiektów (bez gracza), które choć częściowo leżą w zadanym
    # przedziale na osi x
    def get_sprite_group_in_xx(self, x_start, x_end):
        group = py.sprite.Group()

        for item in self._moving_platforms:
            if x_start < item.get_x() + item.get_width():
                if x_end > item.get_x():
                    group.add(item)
            elif x_start < item.get_path_max_x() + item.get_width():
                if x_end > item.get_path_max_x():
                    group.add(item)

        for platform in self._platforms:
            if x_start < platform.get_x() + platform.get_width():
                if x_end > platform.get_x():
                    platform.add(platform)

        for crate in self._crates:
            if x_start < crate.get_x() + crate.get_width():
                if x_end > crate.get_x():
                    group.add(crate)

        for enemy in self._enemies:
            if x_start < enemy.get_x() + enemy.get_width():
                if x_end > enemy.get_x():
                    group.add(enemy)

        for line in self._finish_lines:
            if x_start < line.get_x() + line.get_width():
                if x_end > line.get_x():
                    group.add(line)

            elif x_start < enemy.get_path_max_x() + enemy.get_width():
                if x_end > enemy.get_path_max_x():
                    group.add(enemy)

        return group

    # Settery
    def set_surface_size(self, new_width, new_height):
        self._surface_height = new_height
        self._surface_width = new_width

    # Add
    def add_player(self, player):
        self._player = player

    def add_crate(self, crate):
        self._crates.append(crate)

    def add_moving_platform(self, moving_platform):
        self._moving_platforms.append(moving_platform)

    def add_platform(self, platform):
        self._platforms.append(platform)

    def add_enemy(self, enemy):
        self._enemies.append(enemy)

    def add_finish_line(self, line):
        self._finish_lines.append(line)

    def refresh_mini_platforms(self):
        self._mini_platforms = self.create_mini_platforms()