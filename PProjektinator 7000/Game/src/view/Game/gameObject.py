import pygame as py
import os
from src.enum.objectType import ObjectType

class GameObject(py.sprite.Sprite):
    """Bazowa klasa obiektów w modelu - platform, gracza i obiektów dynamicznych"""
    def __init__(self, x, y, width, height, type, image_source, animation_start = 0):
        super().__init__()
        self.direction = False
        self.type = type
        
        self.width = width
        self.height = height

        self.surf = py.Surface((width, height))
        self.frame_id = 0 #Wskaźnik na obecną klatkę.
        self.animation_start = animation_start #Wskaźnik na klatkę od której zaczyna się animacja.
        self._frames = list()
        #obrazek
        if (image_source != None):
            for name in os.listdir(image_source):
                self._frames.append(os.path.join(image_source,name))
            self.surf = py.image.load(open(self._frames[self.frame_id], "r"))
            self.surf = py.transform.scale(self.surf, (width, height))
            #self.surf.set_colorkey((255, 255, 0))
        else:
            self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.move_ip(x, y)

    #v----GETTERY----v
    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y
    
    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_image(self):
        return self._image

    def get_type(self):
        return self.type

    def get_surf(self):
        return self.surf

    def get_rect(self):
        return self.rect

    #v----SETTERY----v
    #robię setter z dostosowaniem do aktualnego stanu rzeczy - Kanji
    def set_pos(self, newX, newY):
        self.rect.x = newX
        self.rect.y = newY


    def set_frame_by_id(self, frame_id):
        if frame_id >= len(self._frames):
            self.frame_id = self.animation_start
        else:
            self.frame_id = frame_id
        self.surf = py.image.load(open(self._frames[self.frame_id], "r"))
        self.surf = py.transform.smoothscale(self.surf, (self.width, self.height))

    #v----POZOSTAŁE----v
    def check_collision_ip(self, target, x, y):
        return ((target.rect.x < self.rect.x + x + self.rect.width) \
           and (target.rect.x + target.rect.width > self.rect.x + x))\
           and ((target.rect.y < self.rect.y + y + self.rect.height)\
           and (target.rect.y + target.rect.height > self.rect.y + y))

    def check_collision_ip_below(self, target, x, y):
        return target.rect.y < self.rect.y + y + self.rect.height \
           and target.rect.y + 15 > self.rect.y + self.rect.height \
           and target.rect.x < self.rect.x + x + self.rect.width \
           and target.rect.x + target.rect.width > self.rect.x + x


    def update(self):
        pass

    #metoda służąca do zapisywania do pliku aktualnego stanu obiektu 
    def save_to_file(self, file):
        file.write('@<JAKIEŚ ID>')
        file.write('#direction\n' + str(self.direction) + '\n')
        file.write('#type\n' + str(self.type) + '\n')
        #file.write('#spd_x\n' + str(self.spd_x) + '\n')
        #file.write('#spd_x_other\n' + str(self.spd_x_other) + '\n')
        #file.write('#spd_y\n' + str(self.spd_y) + '\n')
        #file.write('#spd_y_other\n' + str(self.spd_y_other) + '\n')
        file.write('#width\n' + str(self.width) + '\n')
        file.write('#height\n' + str(self.height) + '\n')
        file.write('#does_gravity\n' + str(self.does_gravity) + '\n')
        file.write('#frame_id\n' + str(self.frame_id) + '\n')

    #metoda służąca do wczytania z pliku zapisanego stanu obiektu 
    def load_from_file(self, file):
        #trzeba pamiętać, że ta metoda nie ustawia wszystkich pól! (surf, image)
        #TODO - uzupełnić???

        #liczba pól, które wczytujemy
        fieldsCount = 10
        #licznik wczytanych wartości
        counter = 0
        #tablica wczytanych wierszy
        lines = []

        #wczytanie wszytkich wierszy z pominięciem komentarzy
        for line in file:
            if line[0] != '#':
                lines.append(line)
                counter += 1
                if counter == fieldsCount:
                    break

        #przypisanie wczytanych wartości
        self.direction = bool(lines[0])
        self.type = ObjectType(lines[1])
        self.spd_x = float(lines[2])
        self.spd_x_other = float(lines[3])
        self.spd_y = float(lines[4])
        self.spd_y_other = float(lines[5])
        self.width = int(lines[6])
        self.height = int(lines[7])
        self.frame_id = int(lines[8])
        self.does_gravity = bool(lines[9])

