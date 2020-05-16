from .control import Control
from .text import Text
from src.enum.command import Command
import pygame as py


#klasa reprezentująca przycisk w GUI
class Button(Control):

    def __init__(self, text, textSize, pos, hasFrame, command = Command.CONTINUE, primaryColour = (255, 255, 255), secondaryColour = (240, 240, 240)):
        super().__init__(pos, command)

        #przypisanie kolorów
        self._colours[0] = primaryColour
        self._colours[1] = secondaryColour
        
        #stworzenie obiektu odpowiedzialnego za tekst
        self.__text = Text(text, textSize, pos, primaryColour, secondaryColour)

        #ustalenie rozmiaru przycisku ze względu na zajmowane przez tekst miejsce
        self._size = self.__text.get_size()
        
        #ewentualne obramowanie przycisku
        self.__hasFrame = hasFrame
        if hasFrame:
            #miejsce na ramkę to 10 pikseli od tekstu
            tmp = list(self._pos)
            tmp[0] -= 10
            tmp[1] -= 10
            self._pos = tuple(tmp)

            tmp = list(self._size)
            tmp[0] += 20
            tmp[1] += 20
            self._size = tuple(tmp)

    #metoda do aktualizowania stanu kontrolki, np. zmiany koloru
    def update(self):
        #pobranie pozycji kursora
        mousePos = py.mouse.get_pos()
        if mousePos[0] >= self._pos[0] and mousePos[0] <= self._pos[0] + self._size[0] and mousePos[1] >= self._pos[1] and mousePos[1] <= self._pos[1] + self._size[1]:
            self._isFocused = 1
            self.__text.set_is_focused(1)
        else: 
            self._isFocused = 0
            self.__text.set_is_focused(0)

    #metoda do wyrysowania kontrolki
    def draw(self, surface):
        self.__text.draw(surface)
        if self.__hasFrame:
            py.draw.rect(surface, self._colours[self._isFocused], py.Rect(self._pos, self._size), 1)

    # gettery | settery
    def get_text(self):
        return self.__text.get_text()

    def set_text(self, text):
        self.__text.set_text(text)
        self._size = self.__text.get_size()
        if self.__hasFrame:
            tmp = list(self._size)
            tmp[0] += 20
            tmp[1] += 20
            self._size = tuple(tmp)

    def set_pos(self, pos):
        self._pos = pos
        self.set_text_pos(pos)

    def set_text_pos(self, pos):
        if self.__hasFrame:
            self.__text.set_pos(((pos[0] + 10), (pos[1] + 10)))
        else:
            self.__text.set_pos(pos)

    def get_primary_colour(self):
        return self._colours[0]
    
    def set_primary_colour(self, colour):
        self._colours[0] = colour
