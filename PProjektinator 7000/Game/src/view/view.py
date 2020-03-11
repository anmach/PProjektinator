from abc import ABC, abstractmethod
import pygame as py


class View(ABC):

    def __init__(self, surface, surfaceSize = (1600, 900)):
        self._surfaceSize = surfaceSize
        self._surface = surface

    @abstractmethod
    def render(self):
        pass
    
    @abstractmethod
    def setModel(self):
        pass