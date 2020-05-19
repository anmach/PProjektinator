from .control import Control
from src.enum.command import Command
from .button import Button
import src.define as define
import pygame as py

class ImageButtonGroup(Control):
    """może potem dodam opis, ogólnie to to jest taka siatka z możliwością przewijania dostępnych przycisków"""

    def __init__(self, position, command, size, img_buttons=[], division=(1, 1), direction=1):
        """metoda inicjalizująca, znaczenie argumentów:
        positon - pozycja, para (x, y)
        size - rozmiar siatki
        buttons - lista przycisków
        division - liczba kolumn i wierszy
        direction - kierunek przesuwania, 0 - pionowo, 1 - poziomo"""

        super().__init__(position, command, size)

        self.__cell_size = (self._size[0], self._size[1])
        self.__img_buttons = img_buttons
        self.__direction = direction
        self.__division = division
        
        #klikanie slide buttonów - ms
        self.__cooldown = 500
        self.__prev_time = 0
        self.__current_time = 0

        #dodać skalowanie
        self.__extra_size = 50

        #pionowo
        if direction == 0:
            self._size = (self._size[0] * division[0] + self.__extra_size, self._size[1] * division[1])
        #poziomo
        else:
            self._size = (self._size[0] * division[0], self._size[1] * division[1] + self.__extra_size)

        self._prev_button = Button("", 20, (0, 0), False, Command.PREV_OBJECTS)
        self._next_button = Button("", 20, (0, 0), False, Command.NEXT_OBJECTS)

        self.__init_slide_buttons()

        #0 - bez przesunięcia przycisków w siatce
        self.__slide_offset = 0

    def __init_slide_buttons(self):
        #pionowo
        if self.__direction == 0:
            self._prev_button.set_text("^")
            self._prev_button.set_pos((self._pos[0] + self._size[0], self._pos[1]))
            self._next_button.set_text("v")
            self._next_button.set_pos((self._pos[0] + self._size[0], self._pos[1] + self._size[1] // 2))
        #poziomo
        else:
            self._prev_button.set_text("<")
            self._prev_button.set_pos((self._pos[0] + self._size[0] // 4 - self._prev_button.get_size()[0], self._pos[1] + self._size[1] - self.__extra_size))
            self._next_button.set_text(">")
            self._next_button.set_pos((self._pos[0] + 3 * self._size[0] // 4 , self._pos[1] + self._size[1] - self.__extra_size))

    #metoda do aktualizowania stanu kontrolki, np.  zmiany koloru
    def update(self):
        self._prev_button.update()
        self._next_button.update()

        self.__current_time = py.time.get_ticks()
        
        #TODO sprawdzić czy nie należy zamienić division
        if py.mouse.get_pressed()[0]:
            if self.__current_time > self.__prev_time + self.__cooldown:
                self.__prev_time = self.__current_time
                if self._prev_button.get_is_focused() and self.__slide_offset > 0:
                    self.__slide_offset -= 1
                elif self._next_button.get_is_focused():
                   if self.__direction == 0 and self.__slide_offset * self.__division[0] + self.__division[0] * self.__division[1] <= len(self.__img_buttons):
                       self.__slide_offset += 1
                   elif self.__direction == 1 and self.__slide_offset * self.__division[1] + self.__division[0] * self.__division[1] <= len(self.__img_buttons):
                       self.__slide_offset += 1

        self._isFocused = False
        for i in range(0, self.__division[0] * self.__division[1]):

            #TODO - poprawić - błąd, gdy wymiar ma wartość 1
            if self.__direction == 0:
                if i + self.__slide_offset * self.__division[0] - 1 >= len(self.__img_buttons):
                    break
                new_x = self._pos[0] + self.__cell_size[0] * (i % self.__division[0])
                new_y = self._pos[1] + self.__cell_size[1] * (i // self.__division[1])

                self.__img_buttons[i + self.__slide_offset * self.__division[0] - 1].set_pos((new_x, new_y))
                self.__img_buttons[i + self.__slide_offset * self.__division[0] - 1].update()

                if self.__img_buttons[i + self.__slide_offset * self.__division[0] - 1].get_is_focused():
                    self._isFocused = True
            else:
                index = i + self.__slide_offset * self.__division[1] - 1
                if i + self.__slide_offset * self.__division[1] >= len(self.__img_buttons):
                    break
                new_x = int(self._pos[0] + self.__cell_size[0] * (i // (self.__division[0] - 1)))
                new_y = int(self._pos[1] + self.__cell_size[1] * (i % self.__division[1]))

                self.__img_buttons[i + self.__slide_offset * self.__division[1]].set_pos((new_x, new_y))
                self.__img_buttons[i + self.__slide_offset * self.__division[1]].update()

                if self.__img_buttons[i + self.__slide_offset * self.__division[1]].get_is_focused():
                    self.set_is_focused(True)

    def set_buttons(self, buttons=[]):
        self.__img_buttons = buttons

    #metoda do wyrysowania kontrolki
    def draw(self, surface):
        self._prev_button.draw(surface)
        self._next_button.draw(surface)

        #TODO - usunąć offset dla img button?
        for i in range(0, self.__division[0] * self.__division[1]):
            if self.__direction == 0:
                #break, gdy przekroczy zakres
                if i + self.__slide_offset * self.__division[0] >= len(self.__img_buttons):
                    break
                self.__img_buttons[i + self.__slide_offset * self.__division[0]].draw(surface)
            else:
                #break, gdy przekroczy zakres
                if i + self.__slide_offset * self.__division[1] >= len(self.__img_buttons):
                    break
                self.__img_buttons[i + self.__slide_offset * self.__division[1]].draw(surface)

        for i in range(0, self.__division[0]):
            for j in range(0, self.__division[1]):
                py.draw.rect(surface, (20, 20, 20), (self._pos[0] + i * self.__cell_size[0], self._pos[1] + j * self.__cell_size[1], self.__cell_size[0], self.__cell_size[1]), 2)
        
    def get_focused_button(self):
        for img_butt in self.__img_buttons:
            if img_butt.get_is_focused():
                return img_butt
        return None

    def get_command(self):
        for img_butt in self.__img_buttons:
            if img_butt.get_is_focused():
                return img_butt.get_command()
        return Command.CONTINUE

    def get_second_command(self):
        for img_butt in self.__img_buttons:
            if img_butt.get_is_focused():
                return img_butt.get_object_info_command()
        return Command.OBJECT_NONE