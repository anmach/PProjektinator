from .gameObject import GameObject
from src.enum.objectType import ObjectType
import pygame as py

class Player(GameObject):
    """Klasa opisująca gracza."""
    def __init__(self, image_source):
        super().__init__(700, 20, 75, 150, True, ObjectType.DYNAMIC, image_source)
        self.isWalking = False
        self.is_crouching = False

    def update(self):
        if self.spd_y > 20:
            self.spd_y = 20
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

    #metoda zaczynająca "kucnięcie"
    def crouch(self):
        self.is_crouching = True
        print ("Crouching start... \n")
        #zmiana obrazka i przesunięcie o różnice wysokości obrazków


    def uncrouch(self):
        self.is_crouching = False
        print ("Crouching stoped... \n")
        #zmiana obrazka na normalny i przesunięcie o różnice wysokości

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
        file.write('#isWalking\n' + str(self.isWalking) + '\n')

    #metoda służąca do wczytania z pliku zapisanego stanu obiektu 
    def load_from_file(self, file):
        #trzeba pamiętać, że ta metoda nie ustawia wszystkich pól! (surf, image)
        #TODO - uzupełnić???

        #liczba pól, które wczytujemy
        fieldsCount = 11
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
        self.isWalking = bool(lines[10])