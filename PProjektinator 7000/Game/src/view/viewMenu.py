from src.view.view import View
from src.view.UI.text import Text
from src.view.UI.button import Button
from src.enum.command import Command
import pygame as py

class ViewMenu(View):

    def __init__(self, surface):
        super().__init__(surface)

        #tablica przycisków
        self.__buttons = []

        #tworzenie przycisków i przypisanie każdego z nich do ogólnej tablicy kontrolek
        self.__buttons.append(Button("Wyjdz", 50, (0.2 * surface.get_size()[0], 0.8 * surface.get_size()[1]), True, Command.EXIT))
        self._controls.append(self.__buttons[-1])

    def render(self):
        #zaktualizowanie stanu kontrolek (np. ich koloru)
        for control in self._controls:
            control.update()

        #wypełnienie ekranu kolorem jasno-niebieskim
        self._surface.fill((200, 220, 250))

        #wyrysowanie wszystkich tekstów na ekran
        for butt in self.__buttons:
            butt.draw(self._surface)

        #ukazanie nowej zawartości użytkownikowi
        py.display.update()

    #w menu nie jest to potrzebne
    def setModel(self):
        pass
