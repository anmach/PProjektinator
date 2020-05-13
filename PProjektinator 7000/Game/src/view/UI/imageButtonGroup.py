from .control import Control
from src.enum.command import Command
from .button import Button
class ImageButtonGroup(Control):
    """może potem dodam opis, ogólnie to to jest taka siatka z możliwością przewijania dostępnych przycisków"""

    def __init__(self, position, command, size, img_buttons = [], division = (1, 1), direction = 1):
        """metoda inicjalizująca, znaczenie argumentów:
        positon - pozycja, para (x, y)
        size - rozmiar siatki
        buttons - lista przycisków
        division - liczba kolumn i wierszy
        direction - kierunek przesuwania, 0 - pionowo, 1 - poziomo"""

        super().__init__(position, command, size)

        #dodać skalowanie
        extra_size = 50
        self._prev_button = Button("", 20, (0, 0), False, Command.PREV_OBJECTS)
        self._next_button = Button("", 20, (0, 0), False, Command.PREV_OBJECTS)

        if direction == 0:
            self._prev_button.set_text("^")
            self._prev_button.set_pos((self._pos[0] + self._size[0], self._pos[1]))
            self._next_button.set_text("v")
            self._prev_button.set_pos((self._pos[0] + self._size[0], self._pos[1] + self._size[1] // 2))
        else:
            self._prev_button.set_text("<")
            self._prev_button.set_pos((self._pos[0], self._pos[1] + self._size[1]))
            self._next_button.set_text(">")
            self._prev_button.set_pos((self._pos[0] + self._size[0] // 2, self._pos[1] + self._size[1]))

        self.__cell_size = (self._size[0] // division[0], self._size[1] // division[1])
        self.__img_buttons = img_buttons
        self.__direction = direction
        self.__division = division

        if direction == 0:
            self.size = (self._size[0] + extra_size, self._size[1])
        else:
            self.size = (self._size[0], self._size[1] + extra_size)

        #0 - bez przesunięcia przycisków w siatce
        self.__slide_offset = 0

    #metoda do aktualizowania stanu kontrolki, np. zmiany koloru
    def update(self):
        self._prev_button.update()
        self._next_button.update()

        for i in range(0, self.__division[0] * self.__division[1]):
            if i >= len(self.__img_buttons):
                break
            if self.__direction == 0:
                self.__img_buttons[i + self.__slide_offset * self.__division[0] - 1].update()
            else:
                self.__img_buttons[i + self.__slide_offset * self.__division[1] - 1].update()

    #metoda do wyrysowania kontrolki
    def draw(self, surface):
        self._prev_button.draw(surface)
        self._next_button.draw(surface)

        for i in range(0, self.__division[0] * self.__division[1]):
            if i >= len(self.__img_buttons):
                break
            if self.__direction == 0:
                self.__img_buttons[i + self.__slide_offset * self.__division[0] - 1].draw(surface)
            else:
                self.__img_buttons[i + self.__slide_offset * self.__division[1] - 1].draw(surface)

    def get_focused_button(self):
        for img_butt in self.__img_buttons:
            if img_butt.get_is_focused():
                return img_butt
        return None