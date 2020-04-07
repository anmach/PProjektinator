from src.view.view import View
from src.view.UI.text import Text
from src.view.UI.button import Button
from src.enum.command import Command
import pygame as py

class ViewOptions(View):

    def __init__(self, surface):
        super().__init__(surface)

        #tablica przycisków
        self.__buttons = []

        #tworzenie przycisków i przypisanie każdego z nich do ogólnej tablicy kontrolek
        self.__buttons.append(Button("Wyjdź", 60, (0.2 * surface.get_size()[0], 0.7 * surface.get_size()[1]), True, Command.EXIT))
        self._controls.append(self.__buttons[-1])

    def render(self):
        #zaktualizowanie stanu kontrolek (np. ich koloru)
        for control in self._controls:
            control.update()

        #wypełnienie ekranu kolorem
        self._surface.fill((250, 200, 190))

        #wyrysowanie wszystkich przycisków na ekran
        for butt in self.__buttons:
            butt.draw(self._surface)

        #ukazanie nowej zawartości użytkownikowi
        py.display.update()

