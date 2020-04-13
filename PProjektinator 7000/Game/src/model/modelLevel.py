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
        self.__player = Player(".\\res\\sprites\\player.png")
        self.telekinesis = False

        self.__all_sprites.add(self.__player)
        
        self.objs.add(crate1)
        self.objs.add(crate2)
        self.objs.add(platform1)
        self.objs.add(platform2)

        for entity in self.objs:
            self.__all_sprites.add(entity)



    def update(self):

        if self._command & Command.TELEKINESIS & ~0x80 :
            self.telekinesis = True
            self.objs.sprites()[1].does_gravity = False
        else:
            self.objs.sprites()[1].does_gravity = True
            self.telekinesis = False

        spd_x = 5 if self._command & Command.GO_RIGHT & ~0x80 else \
                -5 if self._command & Command.GO_LEFT & ~0x80 else \
                0
        if self.telekinesis:
            self.objs.sprites()[1].set_spd_x(spd_x)
            spd_y = 5 if self._command & Command.CROUCH & ~0x80 else \
                    -5 if self._command & Command.JUMP & ~0x80 else \
                    0
            self.objs.sprites()[1].set_spd_y(spd_y)
        else:
            self.__player.set_spd_x(spd_x)
        if self._command == Command.EXIT:
            self._runMode = False

        
        self.__player.spd_y += 1 if self.__player.does_gravity else\
                               0

        for entity in self.objs:
            if entity.type == ObjectType.DYNAMIC:
                entity.spd_y += 1 if entity.does_gravity else\
                                0

        # kolizje
        for entity in self.objs:
            if self.__player.check_collision_ip(entity, 0, self.__player.spd_y):
                self.__player.spd_y = -20 if self._command & Command.JUMP & ~0x80 and (not self.telekinesis) else\
                                        0
            if self.__player.check_collision_ip(entity, self.__player.spd_x, 0):
                self.__player.spd_x = 0

            for dynamic in self.objs:
                if dynamic.type == ObjectType.DYNAMIC and dynamic != entity:
                    if dynamic.check_collision_ip(entity, 0, dynamic.spd_y):
                        dynamic.spd_y = 0

                    if dynamic.check_collision_ip(entity, dynamic.spd_x, 0):
                        dynamic.spd_x = 0

        # update obiektów (pozycji)
        for entity in self.objs:
            entity.update()
        self.__player.update()

#------------END update-----------------------------

    #v----GETTERY----v
    def get_player(self):
        return self.__player

    def get_all_sprites(self):
        return self.__all_sprites
