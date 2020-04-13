from src.view.view import View
from src.view.UI.text import Text
from src.view.UI.button import Button
from src.view.UI.slider import Slider
from src.enum.command import Command
from src.enum.optionKey import OptionKey
import pygame as py

class ViewOptions(View):

    def __init__(self, surface, options = []):
        super().__init__(surface)
        self.__choosen_one_key = 0
        self.__changed_position = 0

        # tablica opcji -- tablica[x] = (optionKey, wartość)
        self._options = options

        # tablica przycisków, tekstu i sliderów
        self.__buttons = []
        self.__texts = []
        self.__sliders = []

        # rozmieszczenie po ekranie tekstu i przycisków ustawień
        text_size = 20
        x_column1 = 0.1
        x_column2 = 0.3
        x_column3 = 0.5
        x_column4 = 0.7
        optionsY = 0.15
        options_y_offset = 0.07

        # tworzenie wyświetlanego tekstu
        self.__texts.append(Text("Ustawienia", 60, (0.35 * surface.get_size()[0], 0.03 * surface.get_size()[1])))

        # kolumna 1 - tekst dotyczący zmiany sterowania
        self.__texts.append(Text("Ruch w lewo", text_size, (x_column1 * surface.get_size()[0], optionsY * surface.get_size()[1])))
        self.__texts.append(Text("Ruch w prawo", text_size, (x_column1 * surface.get_size()[0], (optionsY + 1 * options_y_offset) * surface.get_size()[1])))
        self.__texts.append(Text("Skok", text_size, (x_column1 * surface.get_size()[0], (optionsY + 2 * options_y_offset) * surface.get_size()[1])))
        
        # kolumna 3 - tekst
        self.__texts.append(Text("Rozdzielczość", text_size, (x_column3 * surface.get_size()[0], optionsY * surface.get_size()[1])))
        self.__texts.append(Text("Głośność?", text_size, (x_column3 * surface.get_size()[0], (optionsY + options_y_offset) * surface.get_size()[1])))

        # tworzenie przycisków i przypisanie każdego z nich do ogólnej tablicy kontrolek
        self.__buttons.append(Button("Wyjdź", 60, (0.2 * surface.get_size()[0], 0.7 * surface.get_size()[1]), True, Command.EXIT))
        self._controls.append(self.__buttons[-1])
        self.__buttons.append(Button("Zapisz", 60, (0.4 * surface.get_size()[0], 0.7 * surface.get_size()[1]), True, Command.SAVE_OPTIONS))
        self._controls.append(self.__buttons[-1])
        
        # kolumna 2 - przyciski do zmiany sterowania
        for option in self._options:
            if option[0] == OptionKey.KEY_GO_LEFT:
                self.__buttons.append(Button(str(option[1]), text_size, (x_column2 * surface.get_size()[0], optionsY * surface.get_size()[1]), True, Command.EXIT))
                self._controls.append(self.__buttons[-1])
            elif option[0] == OptionKey.KEY_GO_RIGHT:
                self.__buttons.append(Button(str(option[1]), text_size, (x_column2 * surface.get_size()[0], (optionsY + 1 * options_y_offset) * surface.get_size()[1]), True, Command.EXIT))
                self._controls.append(self.__buttons[-1])
            elif option[0] == OptionKey.KEY_JUMP:
                self.__buttons.append(Button(str(option[1]), text_size, (x_column2 * surface.get_size()[0], (optionsY + 2 * options_y_offset) * surface.get_size()[1]), True, Command.EXIT))
                self._controls.append(self.__buttons[-1])

        # kolumna 4 - slider
            if option[0] == OptionKey.VOLUME:
                self.__sliders.append(Slider((x_column4 * surface.get_size()[0], optionsY * surface.get_size()[1]), option[1]))

    def render(self):
        #zaktualizowanie stanu kontrolek (np. ich koloru)
        for control in self._controls:
            control.update()
        for slider in self.__sliders:
            slider.update()

        #wypełnienie ekranu kolorem
        self._surface.fill((250, 200, 190))

        #wyrysowanie wszystkich przycisków na ekran
        for butt in self.__buttons:
            butt.draw(self._surface)

        for tex in self.__texts:
            tex.draw(self._surface)

        for sli in self.__sliders:
            sli.draw(self._surface)

        #ukazanie nowej zawartości użytkownikowi
        py.display.update()

    # gettery | settery
    def get_sliders(self):
        return self.__sliders

    def get_options(self):
        return self._options

    def set_options(self, new_options):
        self._options = new_options
