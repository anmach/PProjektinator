from src.view.view import View
import pygame as py

class ViewMenu(View):

    def __init__(self, display):
        super().__init__(display)

    def render(self):
        #wypełnienie ekranu kolorem niebieskim
        self._surface.fill((200, 220, 250))

        #wyrenderowanie wszystkiego na ekran
        py.display.flip()

    def setModel(self):
        pass
