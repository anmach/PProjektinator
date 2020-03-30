from .model import Model
from src.model.gameObjects.gameObject import GameObject
from src.enum.command import Command


class ModelLevel(Model):
    """Model poziomu"""

    def __init__(self):
        super().__init__()
        #czytanie levelu z pliku ale jeszcze nie teraz
        #stworzenie sztywnego poziomu
        self.static_objects[0] = GameObject(0, 200, 400, 20, False)     #dwa obiekty statyczne
        self.static_objects[1] = GameObject(100, 20, 20, 400, False)
        self.player = GameObject(10, 10, 20, 20, True)
        self.gravity = 1


    def update(self):
        self.player.set_spd_x(0)
        
        if self._command == Command.GO_RIGHT:
            self.player.set_spd_x(2)
            self._command = Command.CONTINUE
        elif self._command == Command.GO_LEFT:
            self.player.set_spd_x(-2)
            self._command = Command.CONTINUE


        if self.player.does_gravity: 
            self.player.spd_y += 0.1

        for object in self.static_objects:
            if self.player.check_collision_at(object, self.player.x, self.player.y + self.player.spd_y):    #sprawdzenie pionowej kolizji gracza w stronę w którą się porusza
                if self._command == Command.JUMP:   #kolidujesz z podłożem? tak - skocz, nie - nie skacz
                    self.player.set_spd_y(-10)
                else:
                    self.player.set_spd_y(0)
            if self.player.check_collision_at(object, self.player.x + self.player.spd_x, self.player.y):    #sprawdzenie poziomej kolizji gracza w stronę w którą się porusza
                self.player.set_spd_x(0)



