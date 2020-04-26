from .model import Model
from src.view.Game.gameObject import GameObject
from src.view.Game.player import Player
from src.enum.command import Command
from src.enum.objectType import ObjectType
import pygame as py


class ModelLevel(Model):
    """Model poziomu"""

    def __init__(self, level_number):
        super().__init__()
        # czytanie levelu z pliku ale jeszcze nie teraz
        # stworzenie sztywnego poziomu
        platform1 = GameObject(500, 500, 400, 200, False, ObjectType.STATIC, None)
        platform2 = GameObject(200, 300, 200, 400, False, ObjectType.STATIC, None)
        crate1 = GameObject(450, 100, 100, 100, True, ObjectType.DYNAMIC, None)
        crate2 = GameObject(450, 0, 50, 50, True, ObjectType.DYNAMIC, None)
        self.level_number = level_number

        self.objs = py.sprite.Group()
        self.__all_sprites = py.sprite.Group()
        self.__player = Player(".\\res\\sprites\\player\\")
        self.telekinesis = False
        self.tele_idx = 0
        self.tele_objs = [crate1, crate2]
        self.no_jumps = 0

        self.__all_sprites.add(self.__player)
        
        self.__all_sprites.add(crate1)
        self.__all_sprites.add(crate2)
        self.__all_sprites.add(platform1)
        self.__all_sprites.add(platform2)


    def movement(self):
        spd_x = 5 if self._command & Command.GO_RIGHT & ~0x80 else \
                -5 if self._command & Command.GO_LEFT & ~0x80 else \
                0
        
        if self._command & Command.TELEKINESIS & ~0x80 :                # przytrzymane 'R' - działa telekineza
            self.telekinesis = True                                     # w przeciwnym wypadku - sterowanie
            self.tele_objs[self.tele_idx].does_gravity = False
            if self._command & Command.ATTACK & ~0x80:
                self.tele_objs[self.tele_idx].does_gravity = True
                self.tele_idx = (self.tele_idx + 1) % len(self.tele_objs)
            self.tele_objs[self.tele_idx].set_spd_x(spd_x)
            spd_y = 5 if self._command & Command.CROUCH & ~0x80 else \
                    -5 if self._command & Command.JUMP & ~0x80 else \
                    0
            self.tele_objs[self.tele_idx].set_spd_y(spd_y)
        else:
            self.tele_objs[self.tele_idx].does_gravity = True
            self.tele_objs[self.tele_idx].spd_x = 0
            self.telekinesis = False
            self.__player.set_spd_x(spd_x)  
            if self._command & Command.ATTACK & ~0x80:
                bullet = GameObject(self.__player.get_x(), self.__player.get_y(), 10, 5, False, ObjectType.BULLET ^ ObjectType.DYNAMIC, None)
                bull_spd = -10 if self.__player.direction else 10
                bullet.set_spd_x(bull_spd)
                self.__all_sprites.add(bullet)
            if self._command & Command.JUMP & ~0x80:
                if self.no_jumps > 0:
                    self.__player.spd_y = -20
                    self.no_jumps -= 1

        if self._command == Command.EXIT:                               # wyjście
            self._runMode = False

        for entity in self.__all_sprites:
            if entity.type == ObjectType.DYNAMIC:
                entity.spd_y += 1 if entity.does_gravity else\
                                0


    def collisions(self):
        for entity in self.__all_sprites:

            for dynamic in self.__all_sprites:
                if (dynamic.type & ObjectType.DYNAMIC) and dynamic != entity:
                    if dynamic.check_collision_ip(entity, 0, dynamic.spd_y):
                        dynamic.spd_y = 0
                        if dynamic == self.__player:
                            self.no_jumps = 2

                    if dynamic.check_collision_ip(entity, dynamic.spd_x, 0):
                        if not (dynamic.type & ObjectType.BULLET):
                           dynamic.spd_x = 0
                        if dynamic.type & ObjectType.BULLET and entity != self.__player:
                            self.__all_sprites.remove(dynamic)
                            del dynamic


    def update(self):

        self.movement()
        
        # kolizje
        self.collisions()
        # update obiektów (pozycji)
        for entity in self.__all_sprites:
            entity.update()

#------------END update-----------------------------

    #v----GETTERY----v
    def get_player(self):
        return self.__player

    def get_all_sprites(self):
        return self.__all_sprites
