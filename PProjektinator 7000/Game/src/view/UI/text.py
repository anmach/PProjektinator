from .control import Control
import pygame as py
import src.define as define

#klas umożliwiająca wyświetlanie tekstu na ekranie
class Text(Control):

    def __init__ (self, text, textSize, pos, primaryColour = (255, 255, 255), secondaryColour = (240, 240, 240)):
        super().__init__(pos);

        #przypisanie kolorów
        self._colours[0] = primaryColour
        self._colours[1] = secondaryColour

        #tekst i jego rozmiar do wyświetlania
        self.__text = text
        self.__textSize = textSize

        #utworzenie czcionki z pliku
        self.__font = py.font.Font(define.get_raleway_font_path(), self.__textSize)

        #określienie miejsca zajmowanego przez tekst
        self._size = self.__font.size(self.__text)

    #metoda do aktualizowania stanu kontrolki, np. zmiany koloru
    def update(self):
        #pobranie pozycji kurosora myszy
        mousePos = py.mouse.get_pos()
        if mousePos[0] >= self._pos[0] and mousePos[0] <= self._pos[0] + self._size[0] and mousePos[1] >= self._pos[1] and mousePos[1] <= self._pos[1] + self._size[1]:
            self._isFocused = 1
        else: 
            self._isFocused = 0

    #metoda do wyrysowania kontrolki
    def draw(self, surface):
        self._surface = self.__font.render(self.__text, True, self._colours[self._isFocused])
        surface.blit(self._surface, self._pos)

    def set_text(self, text):
        self.__text = text
        self._size = self.__font.size(self.__text)

    def get_text(self):
        return self.__text