from .gameObject import GameObject
import pygame as py

class Player(GameObject):
    """Klasa opisująca gracza."""
    def __init__(self, image_source):
        super().__init__(700, 20, 50, 50, True, image_source)

    def update(self):
        if self.rect.right < 0:
            self.spd_x=0
            self.rect.move_ip(0, self.y)
        elif self.rect.top < 0:
            self.spd_y=0
            self.rect.move_ip(self.x, 0)
        elif self.rect.left > 1000:
            self.spd_x=0
            self.rect.move_ip(1000, self.y)
        elif self.rect.bottom > 700:
            self.spd_y=0
            self.rect.move_ip(self.x, 700)