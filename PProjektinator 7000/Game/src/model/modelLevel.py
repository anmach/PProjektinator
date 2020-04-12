from .model import Model
from src.view.Game.gameObject import GameObject
from src.view.Game.player import Player
from src.enum.command import Command
import pygame as py


class ModelLevel(Model):
    """Model poziomu"""

    def __init__(self, level_number):
        super().__init__()
        #czytanie levelu z pliku ale jeszcze nie teraz
        #stworzenie sztywnego poziomu
        platform1 = GameObject(500, 500, 400, 200, False, None)     #dwa obiekty statyczne
        platform2 = GameObject(200, 300, 200, 400, False, None)
        moving_obj1 = GameObject(700, 100, 100, 100, True, None)
        self.level_number = level_number

        self.dynamic_objs = py.sprite.Group()
        self.platforms = py.sprite.Group()
        self.enemies = py.sprite.Group()
        self.__all_sprites = py.sprite.Group()
        self.__player = Player(".\\res\\sprites\\player.png")

        self.__all_sprites.add(self.__player)
        
        self.dynamic_objs.add(moving_obj1)
        self.platforms.add(platform1)
        self.platforms.add(platform2)

        for entity in self.dynamic_objs:
            self.__all_sprites.add(entity)
        for entity in self.platforms:
            self.__all_sprites.add(entity)
        for entity in self.__all_sprites:
            entity.rect.move_ip(entity.x, entity.y)


    def update(self):

        spd_x = 5 if self._command & Command.GO_RIGHT & ~0x80 else \
                -5 if self._command & Command.GO_LEFT & ~0x80 else \
                0
        self.__player.set_spd_x(spd_x)

        if self._command == Command.EXIT:
            self._runMode = False

        if self.__player.does_gravity: 
            self.__player.spd_y += 1

    #nie ruszać - magia XD, Ale serio to działa w ten sposób więc nie zmieniajcie tego na razie proszę - Marbi
        self.__player.rect.move_ip(self.__player.spd_x, 0)
        self.__player.rect.move_ip(0, self.__player.spd_y)
        for entity in self.platforms:
            if py.sprite.collide_rect(self.__player, entity):
                self.__player.rect.move_ip(0, -self.__player.spd_y)
                spd_y = -20 if self._command & Command.JUMP & ~0x80 else \
                        0
                self.__player.set_spd_y(spd_y)
            if py.sprite.collide_rect(self.__player, entity):
                self.__player.rect.move_ip(-self.__player.spd_x,0)
                self.__player.set_spd_x(0)

        for entity in self.dynamic_objs:
            if py.sprite.collide_rect(self.__player, entity):
                self.__player.rect.move_ip(0, -self.__player.spd_y)
                spd_y = -20 if self._command & Command.JUMP & ~0x80 else \
                        0
                self.__player.set_spd_y(spd_y)
            if py.sprite.collide_rect(self.__player, entity):
                self.__player.rect.move_ip(-self.__player.spd_x,0)
                self.__player.set_spd_x(0)
                
        
        for dynamic in self.dynamic_objs:
            if dynamic.does_gravity:
                dynamic.set_spd_y(dynamic.get_spd_y()+1)
            dynamic.rect.move_ip(dynamic.spd_x, dynamic.spd_y)
            for entity in self.platforms:
                if py.sprite.collide_rect(dynamic, entity):
                    dynamic.rect.move_ip(0, -dynamic.spd_y)
                    dynamic.set_spd_y(0)
                if py.sprite.collide_rect(dynamic, entity):
                    dynamic.rect.move_ip(-dynamic.spd_x,0)
                    dynamic.set_spd_x(0)
        
        #self.__player.update()

#------------END update-----------------------------

    #v----GETTERY----v
    def get_player(self):
        return self.__player

    def get_all_sprites(self):
        return self.__all_sprites
