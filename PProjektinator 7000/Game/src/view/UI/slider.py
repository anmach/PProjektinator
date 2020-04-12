from .control import Control
from .text import Text
import pygame as py

class Slider(Control):
    """ Klasa reprezentująca... slider """

    def __init__(self, bar_position, initial_value = 0, values = (0, 100), bar_size = (200,20), control_size = (20,30), primary_colour = (180, 150, 200), secondary_colour = (240, 240, 240), bar_colour = (200, 100, 120)):
        super().__init__()

        # suwak został naciśnięty i nie należy zwalniac podświetlenia
        self._is_pushed = 0

        # przypisanie kolorów
        self._colours[0] = primary_colour
        self._colours[1] = secondary_colour
        self._bar_colour = bar_colour

        # pozycja i wielkość paska 
        self._bar_position = bar_position
        self._bar_size = bar_size
        
        # minimalna i maksymalna wartość na sliderze
        self._values = values
        # co ile przesuwa się kontrolka
        self._change = self._bar_size[0]/(self._values[1] - self._values [0])

        # aktualna wartość na sliderze
        if initial_value < self._values[0] or initial_value > self._values[1]:
            self._current_value = self._values[0]
        else:
            self._current_value = initial_value
        
        # pozycja i wielkość kontrolki
        self._size = control_size
        pos_x = self._bar_position[0] + self._change * self._current_value - control_size[0]/2
        pos_y = self._bar_position[1] + self._bar_size[1]/2 - control_size[1]/2
        self._pos = (pos_x, pos_y)

    # metoda do aktualizowania stanu slidera, np. zmiany koloru
    def update(self):
        #pobranie pozycji kursora
        if self._is_pushed == 0:
            mousePos = py.mouse.get_pos()
            if mousePos[0] >= self._pos[0] and mousePos[0] <= self._pos[0] + self._size[0] and mousePos[1] >= self._pos[1] and mousePos[1] <= self._pos[1] + self._size[1]:
                self._isFocused = 1
            else: 
                self._isFocused = 0

    # metoda do wyrysowania slidera
    def draw(self, surface):
        # narysowanie paska
        py.draw.rect(surface, self._bar_colour, py.Rect(self._bar_position, self._bar_size))

        # narysowanie kontrolki
        py.draw.rect(surface, self._colours[self._isFocused], py.Rect(self._pos, self._size), 1)

    def move_right(self):
        if self._current_value < self._values[1]:
            self._current_value += 1
            self._pos = (self._pos[0] + self._change, self._pos[1])
        
    def move_left(self):
        if self._current_value > self._values[0]:
            self._current_value -= 1
            self._pos = (self._pos[0] - self._change, self._pos[1])

    # analiza pozycji kursora i zwiększanie/zmniejszanie wartości na jej podstawie
    def move(self):        
        mouse_position = py.mouse.get_pos()

        if mouse_position[0] > (self._pos[0] + self._size[0]/2):
            self.move_right()
        elif mouse_position[0] < (self._pos[0] + self._size[0]/2):
            self.move_left()

    def get_current_value(self):
        return self._current_value

    def set_is_pushed(self, new_is_pushed):
        self._is_pushed = new_is_pushed



