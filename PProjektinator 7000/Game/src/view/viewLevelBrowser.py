from .view import View
from src.view.UI.text import Text
from src.view.UI.button import Button
from src.enum.command import Command
import pygame as py

class ViewLevelBrowser(View):

    def __init__(self, surface):
        super().__init__(surface)

        #TODO - co powinien wiedzieć widok o modelu, że go wyświetlić? propozycja - wystarczy rysunek poglądowy, ale czy robiony jest automatycznie 
        #na podstawie poziomu czy sami go dostarczamy (jako osobny plik)?
        self.__shownLevel = 0

        #tablica przycisków
        self.__buttons = []
        self.__texts = []

        # ważne rozmiary
        surface_size_x = surface.get_size()[0]
        surface_size_y = surface.get_size()[1]
        button_size = int(0.04 * surface_size_x)

        #tworzenie przycisków i przypisanie każdego z nich do ogólnej tablicy kontrolek
        self.__buttons.append(Button("Wyjdz", button_size, (0.8 * surface_size_x, 0.8 * surface_size_y), True, Command.EXIT))
        self._controls.append(self.__buttons[-1])

        self.__buttons.append(Button("Graj", button_size, (0.42 * surface_size_x, 0.7 * surface_size_y), True, Command.PLAY))
        self._controls.append(self.__buttons[-1])

        #propozycja - dodać nową klasę kontrolek, gdzie nie ma tekstu tylko grafika
        self.__buttons.append(Button("->", button_size, (0.7 * surface_size_x, 0.4 * surface_size_y), True, Command.NEXT_LEVEL))
        self._controls.append(self.__buttons[-1])

        self.__buttons.append(Button("<-", button_size, (0.2 * surface_size_x, 0.4 * surface_size_y), True, Command.PREV_LEVEL))
        self._controls.append(self.__buttons[-1])

        #tekst wyświetlający aktualnie wybrany poziom
        self.__texts.append(Text("", button_size, (0.45 * surface_size_x, 0.385 * surface_size_y)))
        self._controls.append(self.__texts[-1])

    #metoda renderująca
    def render(self):
        #zaktualizowanie stanu kontrolek (np. ich koloru)
        for control in self._controls:
            control.update()

        #wypełnienie ekranu kolorem jasno-niebieskim
        self._surface.fill((200, 220, 250))

        #wyrysowanie wszystkich przycisków na ekran
        for butt in self._controls:
            butt.draw(self._surface)

        #ukazanie nowej zawartości użytkownikowi
        py.display.update()
    

    #v----SETTERY----v
    def set_shown_level(self, shownLevel):
        self.__shownLevel = shownLevel
        self.__texts[0].set_text(str(shownLevel))
