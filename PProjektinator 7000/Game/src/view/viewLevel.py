from src.view.view import View
from src.view.UI.text import Text
from src.view.UI.button import Button
from src.enum.command import Command
from .Game.player import Player
import pygame as py

class ViewLevel(View):
    """Klasa widoku poziomu gry."""
    def __init__(self, surface):
        super().__init__(surface)
        self.__all_sprites = py.sprite.Group()

    def render(self):
        self._surface.fill((200, 220, 250))
        for entity in self.__all_sprites:
            self._surface.blit(entity.surf, entity.rect)
        #self._surface.blit(self.__player)

        py.display.flip()

    #v----GETTERY----v
    def set_player(self, player):
        self.__player = player

    def set_all_sprites(self, all_sprites):
        self.__all_sprites = all_sprites