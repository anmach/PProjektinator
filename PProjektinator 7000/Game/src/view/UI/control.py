from abc import ABC, abstractmethod


#klasa bazowa dla wszelkich kontrolek - przycisków, sliderów, tekstów itp.
class Control(ABC):

    def __init__(self, pos = (0, 0), size = (0, 0), primaryColour = (200,200,200), secondaryColour = (240, 240, 240)):
        #współrzędne - x i y
        self._pos = pos

        #rozmiar - szerokość i wysokość kontrolki - do sprawdzania interakcji z użytkownikiem
        self._size = size

        #tablica kolorów: kolor podstawowy - zwykłe wyświetlanie, drugorzędny - gdy kursor jest nad kontrolką
        self._colours = [primaryColour, secondaryColour]

        #zmienna określająca czy kursor jest nad kontrolką - do indeksowania tablicy colours
        self._colourMode = 0

    #metoda do aktualizowania stanu kontrolki, np. zmiany koloru
    @abstractmethod
    def update(self):
        pass

    #metoda do wyrysowania kontrolki
    @abstractmethod
    def draw(self, surface):
        pass

    #v----SETTERY----v

    def setPos(self, newPos):
        self._pos = newPos

    def setSize(self, newSize):
        self._size = newSize

    #v----GETTERY----v

    def getPos(self):
        return self._pos

    def getSize(self):
        return self._size