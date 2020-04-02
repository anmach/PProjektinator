from abc import ABC, abstractmethod
import pygame as py


class View(ABC):
    """klasa bazowa reprezentująca widok w MVC"""

    def __init__(self, surface, surfaceSize = (1600, 900)):
        #zmienna określająca rozmiar ekranu
        self._surfaceSize = surfaceSize

        self._surface = surface

        #tablica kontrolek
        self._controls = []

    #metoda renderująca
    @abstractmethod
    def render(self):
        pass

    #v----GETTERY----v

    def get_controls(self):
        return self._controls

    def get_surface(self):
        return self._surface
