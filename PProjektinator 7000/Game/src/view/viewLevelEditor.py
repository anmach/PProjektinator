from .view import View

from src.enum.editingMode import EditingMode
from src.enum.command import Command

from src.view.UI.text import Text
from src.view.UI.button import Button

import pygame as py

class ViewLevelEditor(View):

    def __init__(self, surface):
        super().__init__(surface)

        self.__editSurfaceBorder = 0.8

        #tablica przycisków
        self.__buttons = []
        self.__texts = []

        #tworzenie przycisków i przypisanie każdego z nich do ogólnej tablicy kontrolek
        self.__buttons.append(Button("Wyjdz", 50, (0.85 * surface.get_size()[0], 0.9 * surface.get_size()[1]), True, Command.EXIT))
        self._controls.append(self.__buttons[-1])

        #tekst wyświetlający aktualnie wybrany poziom
        self.__texts.append(Text("", 60, (0.85 * surface.get_size()[0], 0.3 * surface.get_size()[1])))
        self._controls.append(self.__texts[-1])

        #wyświetlany nr poziomu
        self.__levelToEdit = 0

        #współrzędne punktów nowej platformy
        self.__newPlatformCoords = (-1, -1)

        #aktualny tryb pracy modelu
        self.__mode = EditingMode.NONE

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

        if self.__mode == EditingMode.PLATFORM_CREATION and py.mouse.get_pos()[0] < self.__editSurfaceBorder * self._surface.get_size()[0]:
            if self.__newPlatformCoords == (-1, -1):
                py.draw.circle(self._surface, (174, 13, 24), py.mouse.get_pos(), 5)
            else:
                x0 = min(self.__newPlatformCoords[0], py.mouse.get_pos()[0])
                x1 = max(self.__newPlatformCoords[0], py.mouse.get_pos()[0])

                y0 = min(self.__newPlatformCoords[1], py.mouse.get_pos()[1])
                y1 = max(self.__newPlatformCoords[1], py.mouse.get_pos()[1])

                py.draw.circle(self._surface, (174, 13, 24), self.__newPlatformCoords, 3)
                py.draw.circle(self._surface, (174, 13, 24), py.mouse.get_pos(), 3)
                py.draw.rect(self._surface, (174, 13, 24), (x0, y0, x1 - x0, y1 - y0), 1)

        #ukazanie nowej zawartości użytkownikowi
        py.display.update()
    

    #v----SETTERY----v
    def set_model(self, levelNum, platCoords, mode):
        self.__texts[0].set_text(str(levelNum))
        self.__newPlatformCoords = platCoords
        self.__mode = mode
