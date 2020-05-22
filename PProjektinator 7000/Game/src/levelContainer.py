import pygame as py
from src.enum.objectType import ObjectType
from src.view.Game.gameObject import GameObject
from src.view.Game.movingPlatform import MovingPlatform

class levelContainer(object):
    """Klasa przechowująca informacje o obiektach znajdujących się w grze"""

    def __init__(self, level_file_name):
        self._level_file_name = file_name
        self._level_number

        self._platforms = []
        self._moving_platforms = []
        self._crates = []

        self._level_read_success = try_load_level_from_file()

    def try_load_level_from_file(self):  
        file = open(self._level_file_name, 'r')

        # Którą z kolei linię danych o obiekcie czytamy
        line_of_object_info = -1

        # Jakie info po kolei zbieramy o obiekcie
        id = -1
        x = -1
        y = -1
        width = -1
        height = -1                
        # Dodatkowe info - KINEMATIC
        movment_max_x = -1
        movment_max_y = -1
        speed_x = -1
        speed_y = -1
                
        # Odczyt kolejnych linii
        for line in file:
            # Usunięcie znaków białych
            stripped_line = line.strip()    

            if stripped_line == "@":
                if line_of_object_info != 0:
                    if try_add_new_object(id, x, y, width, height, type, speed_x, speed_y, movement_max_x, movement_max_y) == 0:
                        # Nie udało się dodać obiektu
                        return 0
                                   
                # Reset danych
                line_of_object_info = 0                
                id = -1
                x = -1
                y = -1
                width = -1
                height = -1                
                movment_max_x = -1
                movment_max_y = -1
                speed_x = -1
                speed_y = -1

            elif line_of_object_info == 0:
                id = int(stripped_line)
                line_of_object_info += 1

            elif line_of_object_info == 1:
                x = int(stripped_line)
                line_of_object_info += 1 

            elif line_of_object_info == 2:
                y = int(stripped_line)
                line_of_object_info += 1
                
            elif line_of_object_info == 3:
                width = int(stripped_line)
                line_of_object_info += 1
                
            elif line_of_object_info == 4:
                height = int(stripped_line)
                line_of_object_info += 1
                
            elif line_of_object_info == 5:
                movment_max_x = int(stripped_line)
                line_of_object_info += 1
                
            elif line_of_object_info == 6:
                speed_y = int(stripped_line)
                line_of_object_info += 1
                
            elif line_of_object_info == 7:
                speed_x = int(stripped_line)
                line_of_object_info += 1
                
            elif line_of_object_info == 8:
                speed_y = int(stripped_line)
                line_of_object_info += 1

            elif stripped_line == "$":
                if try_add_new_object(id, x, y, width, height, type, speed_x, speed_y, movement_max_x, movement_max_y) == 0:
                    # Nie udało się dodać obiektu
                    return 0

            else:
                # Błąd odczytu, za dużo linii
                return 0

        file.close()

        # Udało się odczytać plik poprawnie (chyba)
        return 1

    def try_add_new_object(self, id, x, y, width, height, type, speed_x = -1, speed_y = -1, movement_max_x = -1, movement_max_y = -1):
        if id < 0 or x < 0 or y < 0 or width <= 0 or height <= 0:
            # Błąd - niepoprawne dane
            return 0
        # Dodawanie obiektu
        if id == ObjectType.STATIC:
            self._platforms.append(GameObject(x,y, width, height, False, ObjectType.STATIC, None))
        elif id == ObjectType.DYNAMIC:
            self._crates.append(GameObject(x,y, width, height, True, ObjectType.DYNAMIC, None))
        elif id == ObjectType.KINEMATIC:
            if speed_x < 0 or speed_y < 0 or movment_max_x < 0 or movment_max_y < 0:
                # Błąd - niepoprawne dane
                return 0
            self._moving_platforms.append(MovingPlatform(x,y, width, height, False, ObjectType.KINEMATIC, None, movment_max_x, movment_max_y, speed_x, speed_y))
        else:
            # Błąd - nieznany typ
            return 0

    #Gettery i settery
    def get_level_file_name(self):
        return self._level_file_name

    def get_level_read_succes(self):
        return self._level_read_success

    def get_all_level_objects(self):
        objects = []

        for item in self._platforms:
            objects.append(item)

        for item in self._crates(item):
            objects.append(item)

        for item in self._moving_platforms:
            objects.append(item)

    def get_platforms(self):
        return self._platforms

    def get_crates(self):
        return self._crates

    def get_moving_platforms(self):
        return self._moving_platforms