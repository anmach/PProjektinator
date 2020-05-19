import pygame as py
import time

class BlinkingRect(object):
    """Klasa prostokątu migającego w zadanej częstotliwości"""
    
    def __init__(self, frequency_hz, position, size = (10, 10), colour = (255, 255, 255), colour_secondary = (0, 0, 0)):
        self._displayed_colour = 0
        self._colour = []
        self._colour.append(colour)
        self._colour.append(colour_secondary)

        self._pos = position
        self._size = size
        
        self._changing_time = 1/frequency_hz * 1000
        self._time_to_change = self._changing_time
        self._last_time = py.time.get_ticks()
       
    def update(self):
        self._time_to_change -= (py.time.get_ticks() - self._last_time)
        self._last_time = py.time.get_ticks()

        if self._time_to_change <= 0:
            self.change_displayed_colour()
            self._time_to_change = self._changing_time
        
    def change_displayed_colour(self):
        if self._displayed_colour == 1:
            self._displayed_colour = 0
        else:
            self._displayed_colour = 1

    def draw(self, surface):
        py.draw.rect(surface, self._colour[self._displayed_colour], py.Rect(self._pos, self._size))

