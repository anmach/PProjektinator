from .view import View

from src.enum.editingMode import EditingMode
from src.enum.command import Command

from src.view.UI.text import Text
from src.view.UI.button import Button
from src.view.UI.imageButton import ImageButton

import pygame as py

class ViewLevelEditor(View):

    def __init__(self, surface):
        super().__init__(surface)

        self.__edit_surface_border = 0.8

        #tablica przycisków
        self.__buttons = []
        self.__image_buttons = []
        self.__texts = []

        #tworzenie przycisków, tekstu i przypisanie każdego z nich do ogólnej tablicy kontrolek
        self.add_all_controls()

        #wyświetlany nr poziomu
        self.__levelToEdit = 0

        #współrzędne punktów nowej platformy
        self.__new_platform_first_vertex_pos = (-1, -1)
        self.__new_platform_second_vertex_pos = (-1, -1)

        #aktualny tryb pracy modelu
        self.__mode = EditingMode.NONE

        self.__all_sprites = py.sprite.Group()


    def add_button(self, newButton):
        self.__buttons.append(newButton)
        self._controls.append(newButton)

    def add_text(self, newText):
        self.__texts.append(newText)
        self._controls.append(newText)

    def add_image_button(self, newImageButton):
        self.__image_buttons.append(newImageButton)
        self._controls.append(newImageButton)

    def add_all_controls(self):
        #poziom wcześniej
        self.add_button(Button("<-", 20, (0.82 * self._surface.get_size()[0], 0.02 * self._surface.get_size()[1]), False, Command.PREV_LEVEL))
        
        #tekst wyświetlający aktualnie wybrany poziom
        self.add_text(Text("", 28, (0.89 * self._surface.get_size()[0], 0.015 * self._surface.get_size()[1])))
        
        #poziom dalej
        self.add_button(Button("->", 20, (0.96 * self._surface.get_size()[0], 0.02 * self._surface.get_size()[1]), False, Command.NEXT_LEVEL))
        
        #trzy kolejne raczej wiadomo
        self.add_button(Button("Otwórz", 30, (0.85 * self._surface.get_size()[0], 0.10 * self._surface.get_size()[1]), False, Command.OPEN))

        self.add_button(Button("Nowy", 30, (0.86 * self._surface.get_size()[0], 0.17 * self._surface.get_size()[1]), False, Command.CREATE_NEW))

        self.add_button(Button("Zapisz", 30, (0.855 * self._surface.get_size()[0], 0.24 * self._surface.get_size()[1]), False, Command.SAVE))
        
        #przewijanie kontrolek w lewo
        self.add_button(Button("<-", 20, (0.86 * self._surface.get_size()[0], 0.69 * self._surface.get_size()[1]), False, Command.PREV_LEVEL))

        #dodanie obiektu gracza
        self.add_image_button(ImageButton(".\\res\\sprites\\player\\player.png", (0.81 * self._surface.get_size()[0], 0.5 * self._surface.get_size()[1]), (50, 50), False, Command.OBJECT_SELECTED, Command.PLACE_PLAYER))

        #dodanie obiektu platformy
        self.add_image_button(ImageButton(".\\res\\sprites\\platform tiles\\x3\\tile internal x3.png", (0.90 * self._surface.get_size()[0], 0.5 * self._surface.get_size()[1]), (50, 50), False, Command.OBJECT_SELECTED, Command.CREATE_PLATFORM))

        #przewijanie kontrolek w lewo
        self.add_button(Button("->", 20, (0.92 * self._surface.get_size()[0], 0.69 * self._surface.get_size()[1]), False, Command.NEXT_LEVEL))

        #tez wiadomo
        self.add_button(Button("Wyjdz", 30, (0.86 * self._surface.get_size()[0], 0.93 * self._surface.get_size()[1]), False, Command.EXIT))

    #metoda renderująca
    def render(self):
        #zaktualizowanie stanu kontrolek (np. ich koloru)
        for control in self._controls:
            control.update()

        #wypełnienie ekranu kolorem jasno-niebieskim
        self._surface.fill((200, 220, 250))

        #wyrysowanie wszystkich przycisków na ekran
        for butt in self._controls:
            butt.draw(self._surface)
            
        #linia oddzielająca
        py.draw.line(self._surface, (0,0,0), (self.__edit_surface_border * self._surface.get_size()[0], 0.0), (self.__edit_surface_border * self._surface.get_size()[0], self._surface.get_size()[1]), 5)
        
        #pole edycyjne
        py.draw.rect(self._surface, (240, 240, 240), (0, 0, self.__edit_surface_border * self._surface.get_size()[0], self._surface.get_size()[1]))
        
        for entity in self.__all_sprites:
            self._surface.blit(entity.surf, entity.rect)

        #rysowanie kształtu nowej platformy
        if self.__mode == EditingMode.PLATFORM_CREATION and py.mouse.get_pos()[0] < self.__edit_surface_border * self._surface.get_size()[0]:
            #jeden wierzchołek
            if self.__new_platform_second_vertex_pos == (-1, -1):
                py.draw.circle(self._surface, (174, 13, 24), self.__new_platform_first_vertex_pos, 5)
            #cały prostokąt
            else:
                x0 = min(self.__new_platform_first_vertex_pos[0], self.__new_platform_second_vertex_pos[0])
                x1 = max(self.__new_platform_first_vertex_pos[0], self.__new_platform_second_vertex_pos[0])

                y0 = min(self.__new_platform_first_vertex_pos[1], self.__new_platform_second_vertex_pos[1])
                y1 = max(self.__new_platform_first_vertex_pos[1], self.__new_platform_second_vertex_pos[1])

                py.draw.circle(self._surface, (174, 13, 24), self.__new_platform_first_vertex_pos, 3)
                py.draw.circle(self._surface, (174, 13, 24), self.__new_platform_second_vertex_pos, 3)

                py.draw.rect(self._surface, (0, 0, 0), (x0, y0, x1 - x0, y1 - y0), 1)

        #ukazanie nowej zawartości użytkownikowi
        py.display.update()
    

    #v----GETTERY----v
    def get_image_buttons(self):
        return self.__image_buttons

    #v----SETTERY----v
    def set_model(self, level_num, platform_first_coords, platform_second_coords, mode, all_sprites):
        self.__texts[0].set_text(str(level_num))
        self.__new_platform_first_vertex_pos = platform_first_coords
        self.__new_platform_second_vertex_pos = platform_second_coords
        self.__mode = mode
        self.__all_sprites = all_sprites
