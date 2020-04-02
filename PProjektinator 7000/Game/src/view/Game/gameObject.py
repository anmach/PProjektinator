import pygame as py

class GameObject(py.sprite.Sprite):
    """Bazowa klasa obiektów w modelu - platform, gracza i obiektów dynamicznych"""
    def __init__(self, x, y, width, height, gravity, image_source):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
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

     #v----GETTERY----v
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
    
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

  #  def check_collision_at(self, target, x, y):
   #     if ((x + self.width > target.x) and (x < target.x + target.width)) or ((y + self.height > target.y) and (y < targe.y + target.height)):
    #        return True
     #   else:
      #      return False
