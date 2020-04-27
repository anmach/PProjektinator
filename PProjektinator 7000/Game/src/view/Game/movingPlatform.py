from .gameObject import GameObject

class MovingPlatform(GameObject):
    """description of class"""

    def __init__(self, x, y, width, height, gravity, type, image_source, path_max_x, path_max_y):
        super().__init__(x, y, width, height, gravity, type, image_source)
        self.path_max_x = path_max_x
        self.path_max_y = path_max_y
        self.path_cur_x = 0
        self.path_cur_y = 0


    def update(self):
        super().update()
        self.path_cur_x += self.spd_x
        self.path_cur_y += self.spd_y
        if self.path_cur_x >= self.path_max_x or self.path_cur_x <= 0:
            self.spd_x = -self.spd_x
        if self.path_cur_y >= self.path_max_y or self.path_cur_y <= 0:
            self.spd_y = -self.spd_y

