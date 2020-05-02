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

    #metoda służąca do zapisywania aktualnego stanu obiektu do pliku
    def saveToFile(self, file):
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
        #file.write('#surf\n' + str(self.surf) + '\n')
        file.write('#frame_id\n' + str(self.frame_id) + '\n')
        file.write('#path_max_x\n' + str(self.path_max_x) + '\n')
        file.write('#path_max_y\n' + str(self.path_max_y) + '\n')
        file.write('#path_cur_x\n' + str(self.path_cur_x) + '\n')
        file.write('#path_cur_y\n' + str(self.path_cur_y) + '\n')

