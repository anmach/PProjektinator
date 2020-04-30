import pygame as py
import os

class GameObject(py.sprite.Sprite):
    """Bazowa klasa obiektów w modelu - platform, gracza i obiektów dynamicznych"""
    def __init__(self, x, y, width, height, gravity, type, image_source):
        super().__init__()
        self.direction = False
        self.type = type
        self.spd_x = 0
        self.spd_x_other = 0
        self.spd_y = 0
        self.spd_y_other = 0
        self.width = width
        self.height = height
        self.does_gravity = gravity #bool decyduje czy na obiekt działa grawitacja
        self.surf = py.Surface((width, height))
        self.frame_id = 0 #Wskaźnik na obecną klatkę.
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

    def get_spd_x(self):
        return self.spd_x

    def get_spd_y(self):
        return self.spd_y

    #v----SETTERY----v
    def set_spd_x(self, spd):
        self.spd_x = spd

    def set_spd_y(self, spd):
        self.spd_y = spd

    def set_frame_by_id(self, frame_id):
        if frame_id >= len(self._frames):
            self.frame_id = 1
        else:
            self.frame_id = frame_id
        self.surf = py.image.load(open(self._frames[self.frame_id], "r"))
        self.surf = py.transform.scale(self.surf, (self.width, self.height))

    #v----POZOSTAŁE----v
    def check_collision_ip(self, target, x, y):
        return ((target.rect.x < self.rect.x + x + self.rect.width) \
           and (target.rect.x + target.rect.width > self.rect.x + x))\
           and ((target.rect.y < self.rect.y + y + self.rect.height)\
           and (target.rect.y + target.rect.height > self.rect.y + y))

    def update(self):
        if self.spd_x > 0:
            if self.direction == True:
                self.surf = py.transform.flip(self.surf, True, False)
                self.direction = False
        if self.spd_x < 0:
            if self.direction == False:
                self.direction = True
                self.surf = py.transform.flip(self.surf, True, False)
        self.rect.move_ip(self.spd_x + self.spd_x_other, self.spd_y + self.spd_y_other)
        self.spd_x_other = 0
        self.spd_y_other = 0

