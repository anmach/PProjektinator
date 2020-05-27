from .view import View

from src.enum.editingMode import EditingMode
from src.enum.command import Command
from src.enum.objectType import ObjectType

from src.view.UI.text import Text
from src.view.UI.button import Button
from src.view.UI.imageButton import ImageButton
from src.view.UI.imageButtonGroup import ImageButtonGroup

from src.view.Game.player import Player
from src.view.Game.movingPlatform import MovingPlatform

import pygame as py

import src.define as define

class ViewLevelEditor(View):

    def __init__(self, surface):
        super().__init__(surface)

        self.__edit_surface_border = 0.8

        #tablica przycisków
        self.__buttons = []
        self.__image_buttons = []
        self.__imageButtonGroup = None
        self.__texts = []

        #tworzenie przycisków, tekstu i przypisanie każdego z nich do ogólnej
        #tablicy kontrolek
        self.add_all_controls()

        #wyświetlany nr poziomu
        self.__levelToEdit = 0

        #aktualny tryb pracy modelu
        self.__mode = EditingMode.NONE

        self.__level = []

        #zależy od trybu - info z modelu (współrzędne nowej platformy, gracza,
        #obiektu do usunięcia itp)
        self.__coords = (-1, -1, -1, -1)

        self.__translation = (0, 0)

        self.__can_be_placed = True

    def add_button(self, newButton):
        self.__buttons.append(newButton)
        self._controls.append(newButton)

    def add_text(self, newText):
        self.__texts.append(newText)
        self._controls.append(newText)

    def add_image_button(self, newImageButton):
        self.__image_buttons.append(newImageButton)

    def add_all_controls(self):
        surface_size_x = self._surface.get_size()[0]
        surface_size_y = self._surface.get_size()[1]

        smallest_button_size = int(surface_size_x * 0.016)
        biggest_button_size = int(surface_size_x * 0.024)
        image_button_size = int(surface_size_x * 0.039)

        #poziom wcześniej
        self.add_button(Button("<-", smallest_button_size, (0.82 * surface_size_x, 0.02 * surface_size_y), False, Command.PREV_LEVEL))
        
        #tekst wyświetlający aktualnie wybrany poziom
        self.add_text(Text("", biggest_button_size, (0.89 * surface_size_x, 0.015 * surface_size_y)))
        
        #poziom dalej
        self.add_button(Button("->", smallest_button_size, (0.96 * surface_size_x, 0.02 * surface_size_y), False, Command.NEXT_LEVEL))
        
        #trzy kolejne raczej wiadomo
        self.add_button(Button("Otwórz", biggest_button_size, (0.85 * surface_size_x, 0.10 * surface_size_y), False, Command.OPEN))

        self.add_button(Button("Nowy", biggest_button_size, (0.86 * surface_size_x, 0.17 * surface_size_y), False, Command.CREATE_NEW))

        self.add_button(Button("Zapisz", biggest_button_size, (0.855 * surface_size_x, 0.24 * surface_size_y), False, Command.SAVE))
        
        
        #dodanie obiektu gracza
        self.add_image_button(ImageButton(define.get_player_sprite_path(), (0.81 * surface_size_x, 0.5 * surface_size_y), (image_button_size, image_button_size), False, Command.OBJECT_SELECTED, Command.PLACE_PLAYER))
        
        #dodanie obiektu platformy
        self.add_image_button(ImageButton(define.get_platform_middle_sprite_path(), (0.90 * surface_size_x, 0.5 * surface_size_y), (image_button_size, image_button_size), False, Command.OBJECT_SELECTED, Command.CREATE_PLATFORM))
        
        #dodanie obiektu skrzyni
        self.add_image_button(ImageButton(define.get_crate_sprite_path(), (0.90 * surface_size_x, 0.5 * surface_size_y), (image_button_size, image_button_size), False, Command.OBJECT_SELECTED, Command.PLACE_CRATE))
        
        #dodanie obiektu ruszającej się platformy
        self.add_image_button(ImageButton(define.get_moving_platform_sprite_path(), (0.90 * surface_size_x, 0.5 * surface_size_y), (image_button_size, image_button_size), False, Command.OBJECT_SELECTED, Command.PLACE_MOVING_PLATFORM))

        #żeby było więcej
        self.add_image_button(ImageButton(define.get_platform_middle_sprite_path(), (0.90 * surface_size_x, 0.5 * surface_size_y), (image_button_size, image_button_size), False, Command.OBJECT_SELECTED, Command.CREATE_PLATFORM))
        self.add_image_button(ImageButton(define.get_platform_middle_sprite_path(), (0.90 * surface_size_x, 0.5 * surface_size_y), (image_button_size, image_button_size), False, Command.OBJECT_SELECTED, Command.CREATE_PLATFORM))
        self.add_image_button(ImageButton(define.get_platform_middle_sprite_path(), (0.90 * surface_size_x, 0.5 * surface_size_y), (image_button_size, image_button_size), False, Command.OBJECT_SELECTED, Command.CREATE_PLATFORM))

        self.__imageButtonGroup = ImageButtonGroup((0.825 * surface_size_x, 0.5 * surface_size_y), Command.OBJECT_SELECTED, (image_button_size, image_button_size), self.__image_buttons, (4, 3), 1)
        self._controls.append(self.__imageButtonGroup)

        #usuwanie obiektów
        self.add_button(Button("X", smallest_button_size, (0.892 * surface_size_x, 0.47 * surface_size_y), False, Command.DELETE_OBJECT, (182, 14, 22), (240, 60, 69)))

        #tez wiadomo
        self.add_button(Button("Wyjdz", biggest_button_size, (0.86 * surface_size_x, 0.93 * surface_size_y), False, Command.EXIT))

    #metoda renderująca
    def render(self):
        #zaktualizowanie stanu kontrolek (np.  ich koloru)
        for control in self._controls:
            control.update()

        #wypełnienie ekranu kolorem jasno-niebieskim
        self._surface.fill((200, 220, 250))

        #pole edycyjne
        py.draw.rect(self._surface, (240, 240, 240), (0, 0, self.__edit_surface_border * self._surface.get_size()[0], self._surface.get_size()[1]))
        
        for entity in self.__level.get_sprite_group():
            if isinstance(entity, MovingPlatform):
                py.draw.rect(self._surface, (0,0,0), (entity.get_x() + entity.get_path_max_x(), entity.get_y() + entity.get_path_max_y(), entity.get_width(), entity.get_height()), 1)
                py.draw.line(self._surface, (0,0,0), (entity.get_x() + entity.get_width() // 2, entity.get_y() + entity.get_height() // 2), (entity.get_x() + entity.get_width() // 2 + entity.get_path_max_x(), entity.get_y() + entity.get_height() // 2 + entity.get_path_max_y()), 1)
            self._surface.blit(entity.surf, entity.rect)

        if py.mouse.get_pos()[0] < self.__edit_surface_border * self._surface.get_size()[0]:
            #rysowanie kształtu nowej platformy lub nowej skrzyni
            if self.__mode == EditingMode.PLATFORM_CREATION or self.__mode == EditingMode.CRATE_PLACEMENT:
                #jeden wierzchołek
                if self.__coords[2] == -1:
                    py.draw.circle(self._surface, (174, 13, 24), (self.__coords[0], self.__coords[1]), 5)
                #cały prostokąt
                else:
                    x0 = min(self.__coords[0], self.__coords[2])
                    x1 = max(self.__coords[0], self.__coords[2])

                    y0 = min(self.__coords[1], self.__coords[3])
                    y1 = max(self.__coords[1], self.__coords[3])

                    py.draw.circle(self._surface, (174, 13, 24), (self.__coords[0], self.__coords[1]), 3)
                    py.draw.circle(self._surface, (174, 13, 24), (self.__coords[2], self.__coords[3]), 3)

                    py.draw.rect(self._surface, (0, 0, 0), (x0, y0, x1 - x0, y1 - y0), 1)
            
            #rysowanie obramowania obiektu do usunięcia
            elif self.__mode == EditingMode.DELETION:
                if(self.__coords[0] != -1):
                    py.draw.rect(self._surface, (123, 22, 66), (self.__coords[0], self.__coords[1], self.__coords[2] - self.__coords[0], self.__coords[3] - self.__coords[1]), 3)

            #rysowanie gracza na (potencjalnej) nowej pozycji
            elif self.__mode == EditingMode.PLAYER_PLACEMENT:
                
                new_object = Player(self.__coords[0], self.__coords[1], define.get_player_standard_size()[0], define.get_player_standard_size()[1], True, ObjectType.PLAYER, define.get_player_sprites_folder_path())
                new_object.set_frame_by_id(1)

                self._surface.blit(new_object.surf, new_object.rect)
                if not self.__can_be_placed:
                    py.draw.rect(self._surface, (237, 28, 36), (new_object.get_x(), new_object.get_y(), new_object.get_width(),new_object.get_height()), 3)
                    py.draw.line(self._surface, (237, 28, 36), (new_object.get_x(), new_object.get_y()), (new_object.get_x() + new_object.get_width(), new_object.get_y() + new_object.get_height()), 3)
                    py.draw.line(self._surface, (237, 28, 36), (new_object.get_x() + new_object.get_width(), new_object.get_y()), (new_object.get_x(), new_object.get_y() + new_object.get_height()), 3)
        
            #rysowanie poruszającej się platformy
            elif self.__mode == EditingMode.MOVING_PLATFORM_PLACEMENT:
                #jeden wierzchołek
                if self.__coords[2] == -1:
                    py.draw.circle(self._surface, (174, 13, 24), (self.__coords[0], self.__coords[1]), 5)
                #drugi wierzchołek
                elif self.__coords[4] == -1:
                    x0 = min(self.__coords[0], self.__coords[2])
                    x1 = max(self.__coords[0], self.__coords[2])

                    y0 = min(self.__coords[1], self.__coords[3])
                    y1 = max(self.__coords[1], self.__coords[3])

                    py.draw.circle(self._surface, (174, 13, 24), (self.__coords[0], self.__coords[1]), 3)
                    py.draw.circle(self._surface, (174, 13, 24), (self.__coords[2], self.__coords[3]), 3)

                    py.draw.rect(self._surface, (0, 0, 0), (x0, y0, x1 - x0, y1 - y0), 1)
                #pozycja końcowa
                else:
                    #poz.  pocz.
                    x0 = min(self.__coords[0], self.__coords[2])
                    x1 = max(self.__coords[0], self.__coords[2])

                    y0 = min(self.__coords[1], self.__coords[3])
                    y1 = max(self.__coords[1], self.__coords[3])

                    #poz.  końc.
                    x2 = x0 + self.__coords[4]
                    x3 = x1 + self.__coords[4]

                    y2 = y0 + self.__coords[5]
                    y3 = y1 + self.__coords[5]

                    #pocz.
                    py.draw.rect(self._surface, (0, 0, 0), (x0, y0, x1 - x0, y1 - y0), 1)

                    #końc.
                    py.draw.rect(self._surface, (0, 0, 0), (x2, y2, x3 - x2, y3 - y2), 1)
        
        
        #pole nieedycyjne
        py.draw.rect(self._surface, (200, 220, 250), (self.__edit_surface_border * self._surface.get_size()[0], 0, self._surface.get_size()[0], self._surface.get_size()[1]))
                    
        #wyrysowanie wszystkich przycisków na ekran
        for butt in self._controls:
            butt.draw(self._surface)

        #linia oddzielająca
        py.draw.line(self._surface, (0,0,0), (self.__edit_surface_border * self._surface.get_size()[0], 0.0), (self.__edit_surface_border * self._surface.get_size()[0], self._surface.get_size()[1]), 5)
        
        #ukazanie nowej zawartości użytkownikowi
        py.display.update()
    

    #v----GETTERY----v
    def get_image_buttons(self):
        return self.__image_buttons

    #v----SETTERY----v
    def set_model(self, level_num, mode, level, coords, can_be_placed):
        self.__texts[0].set_text(str(level_num))
        self.__mode = mode
        self.__level = level
        self.__coords = coords
        self.__can_be_placed = can_be_placed

