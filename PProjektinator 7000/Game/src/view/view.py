from abc import ABC, abstractmethod
import pygame as py


#klasa bazowa reprezentująca widok w MVC
class View(ABC):

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

    def getControls(self):
        return self._controls

    def getSurface(self):
        return self._surface