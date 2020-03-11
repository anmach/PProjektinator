from src.view.view import View
from src.view.UI.text import Text
import pygame as py

class ViewMenu(View):

    def __init__(self, surface):
        super().__init__(surface)
        self.__texts = []
        self.__texts.append(Text("Wyjdz", 50, (0.2 * surface.get_size()[0], 0.8 * surface.get_size()[1])))

    def render(self):
        #wypełnienie ekranu kolorem niebieskim
        self._surface.fill((200, 220, 250))

        for text in self.__texts:
            text.draw(self._surface)

        #wyrenderowanie wszystkiego na ekran
        py.display.flip()

    def setModel(self):
        pass
