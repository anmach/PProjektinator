from abc import ABC, abstractmethod
from src.enum.command import Command


#klasa bazowa dla wszelkich kontrolek - przycisków, sliderów, tekstów itp.
class Control(ABC):

    def __init__(self, pos = (0, 0), command = Command.CONTINUE, size = (0, 0), primaryColour = (200,200,200), secondaryColour = (240, 240, 240)):
        #współrzędne - x i y
        self._pos = pos

        #polecenie z danej kontrolki (przekazywane dalej do kontrolera i modelu)
        self._command = command

        #rozmiar - szerokość i wysokość kontrolki - do sprawdzania interakcji z użytkownikiem
        self._size = size

        #tablica kolorów: kolor podstawowy - zwykłe wyświetlanie, drugorzędny - gdy kursor jest nad kontrolką
        self._colours = [primaryColour, secondaryColour]

        #zmienna określająca czy kursor jest nad kontrolką - do indeksowania tablicy colours
        self._isFocused = 0

        #zmienna wykorzystywane przy rysowaniu
        self._surface = None

    #metoda do aktualizowania stanu kontrolki, np. zmiany koloru
    @abstractmethod
    def update(self):
        pass

    #metoda do wyrysowania kontrolki
    @abstractmethod
    def draw(self, surface):
        pass

    #v----SETTERY----v

    def set_pos(self, newPos):
        self._pos = newPos

    def set_size(self, newSize):
        self._size = newSize

    def set_is_focused(self, newState):
        self._isFocused = newState

    #v----GETTERY----v

    def get_pos(self):
        return self._pos

    def get_size(self):
        return self._size

    def get_is_focused(self):
        return self._isFocused

    def get_command(self):
        return self._command