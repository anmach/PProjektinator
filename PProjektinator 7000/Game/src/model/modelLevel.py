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
        platform1 = GameObject(0, 200, 400, 20, False, None)     #dwa obiekty statyczne
        platform2 = GameObject(100, 20, 20, 400, False, None)
        self.level_number = level_number
        self.platforms = py.sprite.Group()
        self.enemies = py.sprite.Group()
        self.__all_sprites = py.sprite.Group()
        self.__player = Player(".\\res\\sprites\\player.png")
        self.__all_sprites.add(self.__player)
        self.__all_sprites.add(platform1)
        self.platforms.add(platform1)
        self.platforms.add(platform2)


    def update(self):
        self.__player.set_spd_x(0)
        
        if self._command == Command.GO_RIGHT:
            self.__player.set_spd_x(2)
            self._command = Command.CONTINUE
        elif self._command == Command.GO_LEFT:
            self.__player.set_spd_x(-2)
            self._command = Command.CONTINUE


        if self.__player.does_gravity: 
            self.__player.spd_y += 0.1

        #for object in self.static_objects:
       #     if self.player.check_collision_at(object, self.player.x, self.player.y + self.player.spd_y):    #sprawdzenie pionowej kolizji gracza w stronę w którą się porusza
        #        if self._command == Command.JUMP:   #kolidujesz z podłożem? tak - skocz, nie - nie skacz
         #           self.player.set_spd_y(-10)
          #      else:
           #         self.player.set_spd_y(0)
        #    if self.player.check_collision_at(object, self.player.x + self.player.spd_x, self.player.y):    #sprawdzenie poziomej kolizji gracza w stronę w którą się porusza
         #       self.player.set_spd_x(0)

    #v----GETTERY----v
    def get_player(self):
        return self.__player

    def get_all_sprites(self):
        return self.__all_sprites


