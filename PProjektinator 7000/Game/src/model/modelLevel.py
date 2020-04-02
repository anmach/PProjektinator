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
        platform1 = GameObject(600, 500, 400, 200, False, None)     #dwa obiekty statyczne
        platform2 = GameObject(200, 300, 200, 400, False, None)
        self.level_number = level_number
        self.platforms = py.sprite.Group()
        self.enemies = py.sprite.Group()
        self.__all_sprites = py.sprite.Group()
        self.__player = Player(".\\res\\sprites\\player.png")
        self.__all_sprites.add(self.__player)
        self.__all_sprites.add(platform1)
        self.__all_sprites.add(platform2)
        self.platforms.add(platform1)
        self.platforms.add(platform2)
        for entity in self.__all_sprites:
            entity.rect.move_ip(entity.x, entity.y)


    def update(self):
        self.__player.set_spd_x(0)
        
        if self._command & Command.GO_RIGHT == Command.GO_RIGHT and not (self._command & 0x80):
            self.__player.set_spd_x(1)
            #self._command = Command.CONTINUE
        elif self._command & Command.GO_LEFT == Command.GO_LEFT and not (self._command & 0x80):
            self.__player.set_spd_x(-1)
            #self._command = Command.CONTINUE
        elif self._command == Command.EXIT:
            self._runMode = False


        if self.__player.does_gravity: 
            self.__player.spd_y += 0.01

        for entity in self.platforms:
            self.__player.rect.move_ip(0, self.__player.spd_y)
            if py.sprite.collide_rect(self.__player, entity):
                if self._command & Command.JUMP == Command.JUMP and not (self._command & 0x80):   #kolidujesz z podłożem? tak - skocz, nie - nie skacz
                    self.__player.set_spd_y(-2)
                else:
                    self.__player.set_spd_y(0)
            self.__player.rect.move_ip(self.__player.spd_x, 0)
            if py.sprite.collide_rect(self.__player, entity):
                self.__player.set_spd_x(0)
        #for entity in self.__all_sprites:
         #   if self.__player.check_collision_at(GameObject, self.__player.x, self.__player.y + self.__player.spd_y):    #sprawdzenie pionowej kolizji gracza w stronę w którą się porusza
          #      if self._command == Command.JUMP:   #kolidujesz z podłożem? tak - skocz, nie - nie skacz
           #         self.__player.set_spd_y(-10)
            #    else:
             #       self.__player.set_spd_y(0)
            #if self.__player.check_collision_at(GameObject, self.__player.x + self.__player.spd_x, self.__player.y):    #sprawdzenie poziomej kolizji gracza w stronę w którą się porusza
             #   self.__player.set_spd_x(0)

            self.__player.update()

    #v----GETTERY----v
    def get_player(self):
        return self.__player

    def get_all_sprites(self):
        return self.__all_sprites


