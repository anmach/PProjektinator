from abc import ABC, abstractmethod
import pygame as py

class Sprite(py.sprite):
    """Klasa bazowa reprezentująca obrazek"""

    def __init__(self, sprite_x, sprite_y, image_source):
        super(Sprite, self).__init__()
        #położenie obrazka
        self._x = sprite_x
        self._y = sprite_y
        
        #obrazek
        self._image = py.image.load(image_source) 

     #v----GETTERY----v
    def get_x(self):
        return self._x

    def get_y(self):
        return self._y
    
    def get_image(self):
        return self._image
