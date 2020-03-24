from .view import View
import pygame as py

class ViewLevelBrowser(View):

    def __init__(self, surface):
        super().__init__(surface)

        #TODO - co powinien wiedzieć widok o modelu, że go wyświetlić? propozycja - wystarczy rysunek poglądowy, ale czy robiony jest automatycznie 
        #na podstawie poziomu czy sami go dostarczamy (jako osobny plik)?
        self.__shownLevel = 0

        #tablica przycisków
        self.__buttons = []

        #tworzenie przycisków i przypisanie każdego z nich do ogólnej tablicy kontrolek
        self.__buttons.append(Button("Wyjdz", 50, (0.4 * surface.get_size()[0], 0.8 * surface.get_size()[1]), True, Command.EXIT))
        self._controls.append(self.__buttons[-1])

        #propozycja - dodać nową klasę kontrolek, gdzie nie ma tekstu tylko grafika
        self.__buttons.append(Button("->", 50, (0.3 * surface.get_size()[0], 0.5 * surface.get_size()[1]), True, Command.EXIT))
        self._controls.append(self.__buttons[-1])

        self.__buttons.append(Button("<-", 50, (0.7 * surface.get_size()[0], 0.5 * surface.get_size()[1]), True, Command.EXIT))
        self._controls.append(self.__buttons[-1])

    #metoda renderująca
    def render(self):
        #zaktualizowanie stanu kontrolek (np. ich koloru)
        for control in self._controls:
            control.update()

        #wypełnienie ekranu kolorem jasno-niebieskim
        self._surface.fill((200, 220, 250))

        #wyrysowanie wszystkich przycisków na ekran
        for butt in self.__buttons:
            butt.draw(self._surface)

        #ukazanie nowej zawartości użytkownikowi
        py.display.update()
    

    #v----SETTERY----v
    def setShownLevel(self, shownLevel):
        self.__shownLevel = shownLevel