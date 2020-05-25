import pygame as py
from src.enum.objectType import ObjectType
from .gameObject import GameObject

class dynamicObject(GameObject):
    """description of class"""

    def __init__(self, x, y, width, height, gravity, type, image_source, animation_start = 0):
        super().__init__(x, y, width, height, type, image_source, animation_start)

        self.spd_x = 0
        self.spd_x_other = 0
        self.spd_y = 0
        self.spd_y_other = 0

        self.does_gravity = gravity


    def get_spd_x(self):
        return self.spd_x


    def get_spd_y(self):
        return self.spd_y


    def set_spd_x(self, spd):
        self.spd_x = spd


    def set_spd_y(self, spd):
        self.spd_y = spd


    def update(self):
        if self.spd_y > 20:
            self.spd_y = 20
        if self.spd_x > 0:
            if self.direction == True:
                self.surf = py.transform.flip(self.surf, True, False)
                self.direction = False
        if self.spd_x < 0:
            if self.direction == False:
                self.direction = True
                self.surf = py.transform.flip(self.surf, True, False)
        self.rect.move_ip(self.spd_x + self.spd_x_other, self.spd_y + self.spd_y_other)
        self.spd_x_other = 0
        self.spd_y_other = 0


    def check_collision_ip(self, target, x, y):
        return ((target.rect.x < self.rect.x + x + self.rect.width) \
           and (target.rect.x + target.rect.width > self.rect.x + x))\
           and ((target.rect.y < self.rect.y + y + self.rect.height)\
           and (target.rect.y + target.rect.height > self.rect.y + y))

    def check_collision_ip_below(self, target, x, y):
        return target.rect.y <= self.rect.y + y + self.rect.height\
           and target.rect.y + 4 >= self.rect.y + self.rect.height \
           and target.rect.x < self.rect.x + x + self.rect.width \
           and target.rect.x + target.rect.width > self.rect.x + x


    def save_to_file(self, file):
        file.write('@<JAKIEŚ ID>')
        file.write('#direction\n' + str(self.direction) + '\n')
        file.write('#type\n' + str(self.type) + '\n')
        file.write('#spd_x\n' + str(self.spd_x) + '\n')
        file.write('#spd_x_other\n' + str(self.spd_x_other) + '\n')
        file.write('#spd_y\n' + str(self.spd_y) + '\n')
        file.write('#spd_y_other\n' + str(self.spd_y_other) + '\n')
        file.write('#width\n' + str(self.width) + '\n')
        file.write('#height\n' + str(self.height) + '\n')
        file.write('#does_gravity\n' + str(self.does_gravity) + '\n')
        file.write('#frame_id\n' + str(self.frame_id) + '\n')

