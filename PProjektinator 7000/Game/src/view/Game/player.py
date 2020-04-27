from .gameObject import GameObject
from src.enum.objectType import ObjectType
import pygame as py

class Player(GameObject):
    """Klasa opisująca gracza."""
    def __init__(self, image_source):
        super().__init__(700, 20, 75, 150, True, ObjectType.DYNAMIC, image_source)
        self.isWalking = False

    def update(self):
        if self.isWalking:
            self.frame_id += 1
        else:
            self.frame_id = 0
        super().set_frame_by_id(self.frame_id)
        if self.spd_x > 0:
            if self.direction == True:
                self.direction = False
            self.isWalking = True
        if self.spd_x < 0:
            if self.direction == False:
                self.direction = True
            self.isWalking = True
        if self.spd_x == 0:
            self.isWalking = False
        self.surf = py.transform.flip(self.surf, self.direction, False)
        self.rect.move_ip(self.spd_x + self.spd_x_other, self.spd_y + self.spd_y_other)
        self.spd_x_other = 0
        self.spd_y_other = 0



