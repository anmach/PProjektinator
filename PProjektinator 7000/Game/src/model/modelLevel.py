from .model import Model
from src.view.Game.gameObject import GameObject
from src.view.Game.dynamicObject import dynamicObject
from src.view.Game.movingObject import MovingObject
from src.view.Game.player import Player
from src.enum.command import Command
from src.enum.objectType import ObjectType
from src.levelContainer import LevelContainer
import pygame as py
import src.define as define

class ModelLevel(Model):
    """Model poziomu"""

    def __init__(self, level_number, display):
        super().__init__()
        
        self.level_number = level_number
        self.__paused = False
        self.__gamover = False
        self.__won = False
        self.__bottomless_pit = 720
        self.__camera = py.Rect(0, 0, display.get_width(), display.get_height())

        self._shot_sound = py.mixer.Sound(define.get_shot_sound_path())

        # TU DODAŁAM
        self._lvl_container = LevelContainer(define.get_levels_folder_path() + "\\001_Tut1.txt", self.level_number)
        self._error = self._lvl_container.get_level_read_succes()

        # Dopasowanie rozmiaru do okna (na razie tylko po y, to zniknie
        self._lvl_container.set_surface_size(display.get_width(), display.get_height())
        self._lvl_container.resize_objects_for_surface_size()

        if self._error != 0:
            self.objs = py.sprite.Group()
            self.__visible_objs = py.sprite.Group()
            self.__player = self._lvl_container.get_player() #= Player(700, 20, 75, 150, True, ObjectType.PLAYER,
                                                             #define.get_player_sprites_folder_path())
            self.update_camera()
            self.telekinesis = False
            self.tele_idx = 0
            self.tele_objs = self._lvl_container.get_crates()
            self.no_jumps = 0

            # TU DODAŁAM
            self.__all_sprites = self._lvl_container.get_sprite_group()
            self.__all_sprites.add(self.__player) 

            # debugowe elementy poziomu
            # self.__all_sprites.add(GameObject(1000, 200, 100, 100,
            # ObjectType.FINISH_LINE, None))
            self.__all_sprites.add(GameObject(700, 500, 1000, 100, ObjectType.STATIC, None))
            # self.__all_sprites.add(MovingObject(1000, 400, 100, 100, False,
            # ObjectType.ENEMY, None, 0, 30, 0, 2))

    def movement(self):
        spd_x = 5 if self._command & Command.GO_RIGHT & ~0x80 else \
                -5 if self._command & Command.GO_LEFT & ~0x80 else \
                0

        for entity in self.__visible_objs:
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
                    for entity in self.__all_sprites:
                        if entity.type == ObjectType.DYNAMIC or entity.type == ObjectType.STATIC:
                            if self.__player.check_collision_ip(entity, 0, 0):
                                self.__player.uncrouch()
                                return
            elif self.__player.is_crouching:
                self.__player.uncrouch()
                for entity in self.__all_sprites:
                    if entity.type == ObjectType.DYNAMIC or entity.type == ObjectType.STATIC:
                        if self.__player.check_collision_ip(entity, 0, 0):
                            self.__player.crouch()
                            return           


    def collisions(self):       # nested 'ifs' to hatch?  xD    #Dobre. #nie, nie dobre
        for entity in self.__all_sprites:
            if entity.rect.x + entity.rect.width > self.__camera.x and entity.rect.x < self.__camera.x + self.__camera.width:
                self.__visible_objs.add(entity)
            else:
                self.__visible_objs.remove(entity)
                if entity.type == ObjectType.DYNAMIC:
                    entity.spd_y = 0

            for dynamic in self.__visible_objs:
                if dynamic != entity and (dynamic.rect.x + dynamic.rect.width > self.__camera.x and dynamic.rect.x < self.__camera.x + self.__camera.width):
                    if ((dynamic.type == ObjectType.DYNAMIC) or (dynamic.type == ObjectType.PLAYER)):
                        if entity.type == ObjectType.KINEMATIC:
                            if dynamic.check_collision_ip_below(entity, 0, dynamic.spd_y + dynamic.spd_y_other):
                                if dynamic.spd_y >= 0:
                                    dynamic.spd_y = 0
                                    dynamic.spd_x_other = entity.spd_x
                                    dynamic.spd_y_other = entity.rect.y - (dynamic.rect.y + dynamic.rect.height)
                                if dynamic == self.__player:
                                    self.no_jumps = 2

                        if (entity.type == ObjectType.STATIC):
                            if dynamic.check_collision_ip(entity, 0, dynamic.spd_y + dynamic.spd_y_other):
                                if dynamic.spd_y + dynamic.spd_y_other > 0:
                                    dynamic.spd_y = entity.rect.y - (dynamic.rect.y + dynamic.rect.height)
                                    dynamic.spd_y_other = 0
                                    if entity.type == ObjectType.DYNAMIC or entity.type == ObjectType.PLAYER:
                                        dynamic.spd_x_other = entity.spd_x + entity.spd_x_other
                                    if dynamic == self.__player:
                                        self.no_jumps = 2
                                if dynamic.spd_y + dynamic.spd_y_other < 0:
                                    dynamic.spd_y = entity.rect.y + entity.rect.height - dynamic.rect.y
                                    dynamic.spd_y_other = 0
                                    if entity.type == ObjectType.DYNAMIC or entity.type == ObjectType.PLAYER:
                                        entity.spd_y = 0
                                        entity.spd_y_other = 0
                            if dynamic.check_collision_ip(entity, dynamic.spd_x + dynamic.spd_x_other, 0):
                                if dynamic.spd_x + dynamic.spd_x_other > 0:
                                    dynamic.spd_x = 0
                                    dynamic.spd_x_other = entity.rect.x - (dynamic.rect.x + dynamic.rect.width)
                                if dynamic.spd_x + dynamic.spd_x_other < 0:
                                    dynamic.spd_x = 0
                                    dynamic.spd_x_other = entity.rect.x + entity.rect.width - dynamic.rect.x

                        if ((entity.type == ObjectType.DYNAMIC) or (entity.type == ObjectType.PLAYER)):
                            if dynamic.check_collision_dynamic(entity, 0, dynamic.spd_y + dynamic.spd_y_other):
                                if dynamic.spd_y + dynamic.spd_y_other > 0:
                                    dynamic.spd_y = entity.get_extended_rect().y - (dynamic.rect.y + dynamic.rect.height) if entity.get_extended_rect().y > dynamic.rect.y + dynamic.rect.height else\
                                                    0
                                    dynamic.spd_y_other = 0
                                    if dynamic == self.__player:
                                        self.no_jumps = 2
                                elif dynamic.spd_y + dynamic.spd_y_other < 0:
                                    dynamic.spd_y = entity.get_extended_rect().y + entity.rect.height - dynamic.rect.y if entity.get_extended_rect().y + entity.rect.height < entity.rect.height else\
                                                    0
                                    dynamic.spd_y_other = 0

                            if dynamic.check_collision_ip(entity, dynamic.spd_x + dynamic.spd_x_other, 0):
                                if dynamic.spd_x + dynamic.spd_x_other > 0:
                                    dynamic.spd_x = 0
                                    dynamic.spd_x_other = entity.rect.x - (dynamic.rect.x + dynamic.rect.width)
                                if dynamic.spd_x + dynamic.spd_x_other < 0:
                                    dynamic.spd_x = 0
                                    dynamic.spd_x_other = entity.rect.x + entity.rect.width - dynamic.rect.x
                        if dynamic.type == ObjectType.PLAYER:
                            if entity.type == ObjectType.FINISH_LINE:
                                    if dynamic.check_collision_ip(entity, 0, 0):
                                        self.__gamover = True
                                        self.__won = True
                            if entity.type == ObjectType.ENEMY:
                                if dynamic.check_collision_ip(entity, 0, 0):
                                        self.__gamover = True
                    if dynamic.type == ObjectType.BULLET and entity != self.__player:
                        if dynamic.check_collision_ip(entity, dynamic.spd_x, dynamic.spd_y):
                            self.__all_sprites.remove(dynamic)
                            self.__visible_objs.remove(dynamic)
                            del dynamic

        if (self.__player.rect.y >= self.__bottomless_pit):
            self.__gamover = True

    def update_camera(self):
        self.__camera.x = self.__player.rect.x - (self.__camera.width / 2)

    def update(self):

        print(self.tele_objs[0].spd_y)
        if self._command == Command.EXIT:                               # wyjście
            self._runMode = False

        if self._error == 0:
            self._runMode = False
            return

        if self._command & Command.PAUSE & ~0x80:
            self.__paused = True if not self.__paused else False

        if not self.__paused and not self.__gamover:
            self.movement()
        # kolizje
            self.collisions()
        # update obiektów (pozycji)
            for entity in self.__visible_objs:
                entity.update()
            self.update_camera()
#------------END update-----------------------------

    #v----GETTERY----v
    def get_player(self):
        return self.__player

    def get_all_sprites(self):
        return self.__visible_objs

    def is_paused(self):
        return self.__paused

    def is_gamover(self):
        return self.__gamover

    def is_won(self):
        return self.__won

    def get_camera(self):
        return self.__camera

