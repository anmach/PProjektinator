from src.enum.command import Command
from .control import Control
import pygame as py

class ButtonsBox(Control):
    """Kontener na przyciski, spośród których jeden przycisk
        jest stale w stanie wciśnięcia"""

    def __init__(self, position, buttons, button_chosen = 0, rows = 1, columns = 1):
        if len(buttons) == 0:
            printf('Brak przyciskow w ButtonsBox\n')
            return

        super().__init__(position, buttons[0].get_command())
        self._buttons = buttons
        self._button_chosen = button_chosen
        # Maksymalna liczba kolumn 
        self._rows = rows
        # Minimalna liczba wierszy
        self._columns = columns

        self._button_height = 0
        self._button_length = 0
        for button in self._buttons:
            if button.get_size()[0] > self._button_length:
                self._button_length = button.get_size()[0]
            if button.get_size()[1] > self._button_height:
                self._button_height = button.get_size()[1]            

        row = -1
        button_index = 0
        button_len = len(self._buttons)

        while button_index < button_len:        
            column = 0
            row += 1
            while column < self._columns:
                self._buttons[button_index].set_size((self._button_length, self._button_height))
                self._buttons[button_index].set_pos((self._pos[0] + column * self._button_length, self._pos[1] + row * self._button_height))
                column += 1
                button_index += 1
                if button_index >= button_len:
                    break  

        if row > self._rows:
            self._rows = row

    #metoda do aktualizowania stanu kontrolki, np. zmiany koloru
    def update(self):
        #pobranie pozycji kursora
        mousePos = py.mouse.get_pos()

        for button in self._buttons:
            if mousePos[0] >= button.get_pos()[0] and mousePos[0] <= button.get_pos()[0] + button.get_size()[0] and mousePos[1] >= button.get_pos()[1] and mousePos[1] <= button.get_pos()[1] + button.get_size()[1]:
                button.set_is_focused(1)
            else: 
                button.set_is_focused(0)
    
    #metoda do wyrysowania kontrolki
    def draw(self, surface):
        for button in self._buttons:
            button.draw(surface)

