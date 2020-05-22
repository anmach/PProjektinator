from src.view.view import View
from src.view.UI.text import Text
from src.view.UI.button import Button
from src.enum.command import Command
from src.view.blinkingRect import BlinkingRect
from .Game.player import Player
import pygame as py

class ViewLevel(View):
    """Klasa widoku poziomu gry."""
    def __init__(self, surface):
        super().__init__(surface)
        self.__all_sprites = py.sprite.Group()
        self.__paused = False
        self.__text = Text("Spauzowano.", int(0.04 * self._surfaceSize[0]), (0.35 * self._surfaceSize[0], 0.05 * self._surfaceSize[1]))
        self.__blink_enabled = true

        self.__blinking_rects = []
        self.__blinking_rects.append(BlinkingRect(0.5, (0.01 * self._surfaceSize[0], 0.01 * self._surfaceSize[0]), (0.02 * self._surfaceSize[0], 0.02 * self._surfaceSize[0])))

    def render(self):
        self._surface.fill((200, 220, 250))
        if self.__paused == True:
            self.__text.draw(self._surface)
        else:
            for entity in self.__all_sprites:
                self._surface.blit(entity.surf, entity.rect)
            if self.__blink_enabled:
                for rect in self.__blinking_rects:
                    rect.update();
                    rect.draw(self._surface)
        #self._surface.blit(self.__player.get_surf(), self.__player.get_rect())

        py.display.flip()

    #v----GETTERY----v
    def set_player(self, player):
        self.__player = player

    def set_all_sprites(self, all_sprites):
        self.__all_sprites = all_sprites

    def set_paused(self, paused):
        self.__paused = paused

    def set_blink_enabled(self, do_we_blink):
        self.__blink_enabled = do_we_blink