from abc import ABC, abstractmethod
import pygame as py
from src.enum.optionKey import OptionKey


class View(ABC):
    """klasa bazowa reprezentująca widok w MVC"""

    def __init__(self, surface):
        #zmienna określająca rozmiar ekranu
        self._surfaceSize = self.get_surface_size_from_file()
        display = py.display.set_mode(self._surfaceSize)

        self._surface = surface

        #tablica kontrolek
        self._controls = []

    #metoda renderująca
    @abstractmethod
    def render(self):
        pass

    #pobranie rozmiaru ekranu z pliku opszyns.txt
    def get_surface_size_from_file(self):
        file = open('.\\saves\\opszyns.txt', 'r')
        width = 1000
        height = 700
        
        # odczyt kolejnych linii
        for line in file:
            splitted_line = line.strip().split()
            int_optionKey = int(splitted_line[0])
            # dodanie informacji do tablicy opcji
            if int_optionKey == OptionKey.WINDOW_WIDTH:
                width = int(splitted_line[1])             
            elif int_optionKey == OptionKey.WINDOW_HEIGHT:                
                height = int(splitted_line[1])

        file.close()
        return (width, height)

    #v----GETTERY----v

    def get_controls(self):
        return self._controls

    def get_surface(self):
        return self._surface
