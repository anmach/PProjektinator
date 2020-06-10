from .dynamicObject import dynamicObject

class MovingObject(dynamicObject):
    """description of class"""

    def __init__(self, x, y, width, height, gravity, type, image_source, path_max_x, path_max_y, spd_x, spd_y):
        super().__init__(x, y, width, height, gravity, type, image_source)
        self.path_max_x = path_max_x
        self.path_max_y = path_max_y
        self.path_cur_x = 0
        self.path_cur_y = 0
        self.spd_x = spd_x
        self.spd_y = spd_y


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
        file.write('#frame_id\n' + str(self.frame_id) + '\n')
        file.write('#path_max_x\n' + str(self.path_max_x) + '\n')
        file.write('#path_max_y\n' + str(self.path_max_y) + '\n')
        file.write('#path_cur_x\n' + str(self.path_cur_x) + '\n')
        file.write('#path_cur_y\n' + str(self.path_cur_y) + '\n')

    #metoda służąca do wczytania z pliku zapisanego stanu obiektu 
    def load_from_file(self, file):
        #trzeba pamiętać, że ta metoda nie ustawia wszystkich pól! (surf, image)
        #TODO - uzupełnić???

        #liczba pól, które wczytujemy
        fieldsCount = 14
        #licznik wczytanych wartości
        counter = 0
        #tablica wczytanych wierszy
        lines = []

        #wczytanie wszytkich wierszy z pominięciem komentarzy
        for line in file:
            if line[0] != '#':
                lines.append(line)
                counter += 1
                if counter == fieldsCount:
                    break

        #przypisanie wczytanych wartości
        self.direction = bool(lines[0])
        self.type = ObjectType(lines[1])
        self.spd_x = float(lines[2])
        self.spd_x_other = float(lines[3])
        self.spd_y = float(lines[4])
        self.spd_y_other = float(lines[5])
        self.width = int(lines[6])
        self.height = int(lines[7])
        self.frame_id = int(lines[8])
        self.does_gravity = bool(lines[9])
        self.path_max_x = int(lines[10])
        self.path_max_y = int(lines[11])
        self.path_cur_x = int(lines[12])
        self.path_cur_y = int(lines[13])

    def get_path_max_x(self):
        return self.path_max_x

    def get_path_max_y(self):
        return self.path_max_y
