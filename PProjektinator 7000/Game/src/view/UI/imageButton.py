from .control import Control
from src.enum.command import Command
import pygame as py


#klasa reprezentująca przycisk w GUI
class ImageButton(Control):

    #size (0, 0) oznacza, że korzystamy z domyślnego rozmiaru obrazu
    #fillScaling - czy skalowanie ma całkowicie wypełnić dany obszar obrazem (True) czy zachować jego proporcje (False)
    def __init__(self, imagePath, pos, size = (0, 0), fillScaling = True, command = Command.CONTINUE):
        super().__init__(pos, command, size)

        #stworzenie obiektu odpowiedzialnego za tekst
        self.__image = py.image.load(imagePath)
        
        if size == (0, 0):
            self.__size = self.__image.get_rect().size
        else:
            self._size = size
            
            if fillScaling == True:
                self.__image = py.transform.scale(self.__image, (size))
            else:
                #obliczenie skali
                scale = min(size[0] / self.__image.get_rect().size[0], size[1] / self.__image.get_rect().size[1])
                
                #skalowanie obrazu
                self._size = (int(self.__image.get_rect().size[0] * scale), int(self.__image.get_rect().size[1] * scale))
                self.__image = py.transform.scale(self.__image, (self._size[0], self._size[1]))
                
        #przesunięcię obrazu na środek
        self.__imageOffset = (size[0] - self.__image.get_rect().size[0], size[1] - self.__image.get_rect().size[1])
            
    #metoda do aktualizowania stanu kontrolki
    def update(self):
        #pobranie pozycji kursora
        mousePos = py.mouse.get_pos()
        if mousePos[0] >= self._pos[0] + self.__imageOffset[0] and mousePos[0] <= self._pos[0] + self.__imageOffset[0] + self._size[0] and mousePos[1] >= self._pos[1] + self.__imageOffset[1] and mousePos[1] <= self._pos[1] + self.__imageOffset[1] + self._size[1]:
            self._isFocused = 1
        else: 
            self._isFocused = 0

    #metoda do wyrysowania kontrolki
    def draw(self, surface):
        surface.blit(self.__image, (self._pos[0] + self.__imageOffset[0], self._pos[1] + self.__imageOffset[1]))
        #rysowanie ramki jako podsietlenia
        if self._isFocused:
            py.draw.rect(surface, (255, 200, 0), (self._pos[0] + self.__imageOffset[0], self._pos[1] + self.__imageOffset[1], self._size[0], self._size[1]), 3)