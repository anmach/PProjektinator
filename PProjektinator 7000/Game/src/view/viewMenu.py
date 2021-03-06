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

        surface_size_x = surface.get_size()[0]
        surface_size_y = surface.get_size()[1]

        button_size = int(0.04 * surface_size_x)

        #tworzenie przycisków i przypisanie każdego z nich do ogólnej tablicy kontrolek
        self.__buttons.append(Button("Wyjdź", button_size, (0.2 * surface_size_x, 0.7 * surface_size_y), True, Command.EXIT))
        self._controls.append(self.__buttons[-1])

        self.__buttons.append(Button("Przeglądaj poziomy", button_size, (0.2 * surface_size_x, 0.5 * surface_size_y), True, Command.BROWSE_LVL))
        self._controls.append(self.__buttons[-1])
        
        self.__buttons.append(Button("Opcje", button_size, (0.2 * surface_size_x, 0.3* surface_size_y), True, Command.OPTIONS))
        self._controls.append(self.__buttons[-1])

        self.__buttons.append(Button("Edytor", button_size, (0.2 * surface_size_x, 0.1* surface_size_y), True, Command.EDIT))
        self._controls.append(self.__buttons[-1])

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
