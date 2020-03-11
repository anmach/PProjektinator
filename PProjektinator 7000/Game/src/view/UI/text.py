from .control import Control
import pygame as py


#klas umożliwiająca wyświetlanie tekstu na ekranie
class Text(Control):

    def __init__ (self, text, textSize, pos, primaryColour = (200, 200, 200), secondaryColour = (240, 240, 240)):
        super().__init__(self, pos);

        #tekst i jego rozmiar do wyświetlania
        self.__text = text
        self.__textSize = textSize

        #utworzenie czcionki z pliku
        self.__font = py.freetype.Font("res/fonts/Raleway.ttf", textSize)

        #określienie miejsca zajmowanego przez tekst
        #self._size = self.font.

    #metoda do aktualizowania stanu kontrolki, np. zmiany koloru
    def update(self):
        mousePos = py.mouse.get_pos()
        if mousePos >= self._pos and mousePos <= self._pos + self._size:
            self._colourMode = 1
        else: 
            self._colourMode = 0

    #metoda do wyrysowania kontrolki
    def draw(self, surface):
        self.__font.render_to(surface, self._pos, self._colours[self._colourMode])