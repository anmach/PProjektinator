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
        self.__gameover = False
        self.__won = False
        self.__camera = None
        self.__pause_text = Text("Spauzowano.", int(0.04 * self._surfaceSize[0]), (0.35 * self._surfaceSize[0], 0.05 * self._surfaceSize[1]))
        self.__won_text = Text("Gratulacje! Naciśnij Esc przy wybrać kolejny poziom.", int(0.04 * self._surfaceSize[0]), (0.05 * self._surfaceSize[0], 0.05 * self._surfaceSize[1]))
        self.__lost_text = Text("YOU DIED. Naciśnij Esc by spróbować ponownie.", int(0.04 * self._surfaceSize[0]), (0.05 * self._surfaceSize[0], 0.05 * self._surfaceSize[1]))
        self.__blink_enabled = 1

        self.__blinking_rects = []
        self.__blinking_rects.append(BlinkingRect(8, (0.01 * self._surfaceSize[0], 0.5 * self._surfaceSize[1]), (0.02 * self._surfaceSize[0], 0.02 * self._surfaceSize[0])))
        self.__blinking_rects.append(BlinkingRect(10, (0.5 * self._surfaceSize[0], 0.01 * self._surfaceSize[1]), (0.02 * self._surfaceSize[0], 0.02 * self._surfaceSize[0])))
        self.__blinking_rects.append(BlinkingRect(12, (0.97 * self._surfaceSize[0], 0.5 * self._surfaceSize[1]), (0.02 * self._surfaceSize[0], 0.02 * self._surfaceSize[0])))
        self.__blinking_rects.append(BlinkingRect(15, (0.5 * self._surfaceSize[0], 0.96 * self._surfaceSize[1]), (0.02 * self._surfaceSize[0], 0.02 * self._surfaceSize[0])))

    def render(self):
        self._surface.fill((200, 220, 250))
        if self.__paused == True:
            self.__pause_text.draw(self._surface)
        elif self.__gameover == True and self.__won == True:
            self.__won_text.draw(self._surface)
        elif self.__gameover == True and self.__won == False:
            self.__lost_text.draw(self._surface)
        else:
            for entity in self.__all_sprites:
                self._surface.blit(entity.surf, (entity.get_x() - self.__camera.x, entity.get_y() - self.__camera.y))
            if self.__blink_enabled == 1:
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

    def set_gameover(self, gameover):
        self.__gameover = gameover

    def set_won(self, won):
        self.__won = won

    def set_camera(self, camera):
        self.__camera = camera

    def set_blink_enabled(self, do_we_blink):
        self.__blink_enabled = do_we_blink