import pygame as py

class GameObject(py.sprite.Sprite):
    """Bazowa klasa obiektów w modelu - platform, gracza i obiektów dynamicznych"""
    def __init__(self, x, y, width, height, gravity, type, image_source):
        super().__init__()
        self.direction = 1
        self.type = type
        self.spd_x = 0
        self.spd_y = 0
        self.does_gravity = gravity #bool decyduje czy na obiekt działa grawitacja
        self.surf = py.Surface((width, height))
        #obrazek
        if (image_source != None):
            self._image = py.image.load(image_source).convert()
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
    
    def get_image(self):
        return self._image

    def get_spd_x(self):
        return self.spd_x

    def get_spd_y(self):
        return self.spd_y

    def set_spd_x(self, spd):
        self.spd_x = spd

    def set_spd_y(self, spd):
        self.spd_y = spd

    def check_collision_ip(self, target, x, y):
        return ((target.rect.x < self.rect.x + x + self.rect.width) \
           and (target.rect.x + target.rect.width > self.rect.x + x))\
           and ((target.rect.y < self.rect.y + y + self.rect.height)\
           and (target.rect.y + target.rect.height > self.rect.y + y))

    def update(self):
        if self.spd_x > 0:
            self.direction = 1
        if self.spd_x < 0:
             self.direction = -1
        self.rect.move_ip(self.spd_x, self.spd_y)