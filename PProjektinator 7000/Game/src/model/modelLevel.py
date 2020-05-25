from .model import Model
from src.view.Game.gameObject import GameObject
from src.view.Game.dynamicObject import dynamicObject
from src.view.Game.movingPlatform import MovingPlatform
from src.view.Game.player import Player
from src.enum.command import Command
from src.enum.objectType import ObjectType
from src.levelContainer import LevelContainer
import pygame as py
import src.define as define

class ModelLevel(Model):
    """Model poziomu"""

    def __init__(self, level_number):
        super().__init__()
        
        self.level_number = level_number

        self.__paused = False
        self._shot_sound = py.mixer.Sound(define.get_shot_sound_path())

        # czytanie levelu z pliku ale jeszcze nie teraz
        # TU DODAŁAM
        self._lvl_container = LevelContainer(define.get_levels_folder_path() + "\\001_Tut1.txt", self.level_number)
        self._error = self._lvl_container.get_level_read_succes()

        if self._error != 0:
            self.objs = py.sprite.Group()
            self.__player = self._lvl_container.get_player() #= Player(700, 20, 75, 150, True, ObjectType.PLAYER, define.get_player_sprites_folder_path())
            self.telekinesis = False
            self.tele_idx = 0
            self.tele_objs = self._lvl_container.get_crates()
            self.no_jumps = 0

            # TU DODAŁAM
            self.__all_sprites = self._lvl_container.get_sprite_group()
            self.__all_sprites.add(self.__player) 

        # debugowe elementy poziomu
        platform1 = GameObject(200, 150, 50, 49, ObjectType.STATIC, None)
        self.__all_sprites.add(platform1)


    def movement(self):
        spd_x = 5 if self._command & Command.GO_RIGHT & ~0x80 else \
                -5 if self._command & Command.GO_LEFT & ~0x80 else \
                0

        for entity in self.__all_sprites:
            if entity.type == ObjectType.DYNAMIC or entity.type == ObjectType.PLAYER:
                entity.spd_y += 1 if entity.does_gravity else\
                                0
        
        if self._command & Command.TELEKINESIS & ~0x80 :                # przytrzymane 'R' - działa telekineza
            self.telekinesis = True                                     # w przeciwnym wypadku - sterowanie
            self.tele_objs[self.tele_idx].does_gravity = False
            if self._command & Command.ATTACK & ~0x80:
                self.tele_objs[self.tele_idx].does_gravity = True
                self.tele_idx = (self.tele_idx + 1) % len(self.tele_objs)
            self.tele_objs[self.tele_idx].set_spd_x(spd_x)
            spd_y = 5 if self._command & Command.CROUCH & ~0x80 else \
                    -5 if self._command & Command.GO_UP & ~0x80 else \
                    0
            self.tele_objs[self.tele_idx].set_spd_y(spd_y)
        else:
            self.tele_objs[self.tele_idx].does_gravity = True
            self.tele_objs[self.tele_idx].spd_x = 0
            self.telekinesis = False
            self.__player.set_spd_x(spd_x)  
            if self._command & Command.ATTACK & ~0x80:      # tu się strzela
                py.mixer.Sound.play(self._shot_sound)
                bullet = dynamicObject(self.__player.get_x(), self.__player.get_y() + 50, 80, 40, False, ObjectType.BULLET, define.get_shot_sprite_folder_path())
                bull_spd = -10 if self.__player.direction else 10
                bullet.set_spd_x(bull_spd)
                self.__all_sprites.add(bullet)
            if self._command & Command.JUMP & ~0x80:
                if self.no_jumps > 0:
                    # *dźwięk skoku*
                    self.__player.spd_y = -20
                    self.no_jumps -= 1
            if self._command & Command.CROUCH & ~0x80:
                if not self.__player.is_crouching:
                    self.__player.crouch()
            elif self.__player.is_crouching:
                self.__player.uncrouch()
                for entity in self.__all_sprites:
                    if entity.type == ObjectType.DYNAMIC or entity.type == ObjectType.STATIC:
                        if self.__player.check_collision_ip(entity, 0, 0):
                            self.__player.crouch()
                            return           


    def collisions(self):       # nested 'ifs' to hatch? xD
        for entity in self.__all_sprites:
            for dynamic in self.__all_sprites:
                if dynamic != entity:
                    if ((dynamic.type == ObjectType.DYNAMIC) or (dynamic.type == ObjectType.PLAYER)):
                        if ((entity.type == ObjectType.STATIC) or (entity.type == ObjectType.DYNAMIC) or (entity.type == ObjectType.PLAYER)):
                            if dynamic.check_collision_ip(entity, 0, dynamic.spd_y):
                                if dynamic == self.__player:
                                    self.no_jumps = 2
                                if dynamic.spd_y > 0:
                                    dynamic.spd_y = entity.rect.y - (dynamic.rect.y + dynamic.rect.height)
                                if dynamic.spd_y < 0:
                                    dynamic.spd_y = entity.rect.y + entity.rect.height - dynamic.rect.y

                            if dynamic.check_collision_ip(entity, dynamic.spd_x, 0):
                                dynamic.spd_x = 0

                        if entity.type == ObjectType.KINEMATIC:
                            if dynamic.check_collision_ip_below(entity, 0, dynamic.spd_y + dynamic.spd_y_other):
                                if dynamic.spd_y >= 0:
                                    dynamic.spd_y = 0
                                    dynamic.spd_x_other = entity.spd_x
                                    dynamic.spd_y_other = entity.rect.y - (dynamic.rect.y + dynamic.rect.height)
                                if dynamic == self.__player:
                                    self.no_jumps = 2

                    if dynamic.type == ObjectType.BULLET and entity != self.__player:
                        if dynamic.check_collision_ip(entity, dynamic.spd_x, dynamic.spd_y):
                            self.__all_sprites.remove(dynamic)
                            del dynamic


    def update(self):

        if self._command == Command.EXIT:                               # wyjście
            self._runMode = False

        if self._error == 0:
            self._runMode = False
            return

        if self._command & Command.PAUSE & ~0x80:
            self.__paused = True if not self.__paused else False

        if not self.__paused:
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

    def is_paused(self):
        return self.__paused
