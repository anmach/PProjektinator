from abc import ABC, abstractmethod
import pygame as py


class View(ABC):

    def __init__(self, display, displaySize):
        this.displaySize = displaySize
        this.display = display

    @abstractmethod
    def render(self):
        pass
    
    @abstractmethod
    def setModel(self):
        pass