from src.view.view import View
from src.view.UI.text import Text
from src.view.UI.button import Button
from src.view.UI.slider import Slider
from src.view.UI.buttonsBox import ButtonsBox
from src.enum.command import Command
from src.enum.optionKey import OptionKey
import pygame as py

class ViewOptions(View):

    def __init__(self, surface, options = []):
        super().__init__(surface)

        # tablica opcji -- tablica[x] = (optionKey, wartość)
        self._options = options

        # tablica przycisków, tekstu i sliderów
        self.__buttons = []
        self.__buttons_optionKeys = [] # opisy przycisków na indeksach odpowiadających tym z wyższej tablicy
        self.__texts = [] 
        self.__sliders = [] # sliders = (OptionKey, Slider)

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
        self.__texts.append(Text("Kucnięcie", text_size, (x_column1 * surface.get_size()[0], (optionsY + 3 * options_y_offset) * surface.get_size()[1])))
        self.__texts.append(Text("Atak", text_size, (x_column1 * surface.get_size()[0], (optionsY + 4 * options_y_offset) * surface.get_size()[1])))
        self.__texts.append(Text("Telekineza", text_size, (x_column1 * surface.get_size()[0], (optionsY + 5 * options_y_offset) * surface.get_size()[1])))
        
        # kolumna 3 - tekst
        self.__texts.append(Text("Głośność", text_size, (x_column3 * surface.get_size()[0], (optionsY) * surface.get_size()[1])))
        self.__texts.append(Text("Rozdzielczość", text_size, (x_column3 * surface.get_size()[0], (optionsY + options_y_offset) * surface.get_size()[1])))
        
        # kolumna 2 - przyciski do zmiany sterowania
        for option in self._options:
            if option[0] == OptionKey.KEY_GO_LEFT:
                self.__buttons.append(Button(chr(option[1]), text_size, (x_column2 * surface.get_size()[0], optionsY * surface.get_size()[1]), True, Command.OPTIONS_CHANGE_KEY))
                self._controls.append(self.__buttons[-1])
                self.__buttons_optionKeys.append(OptionKey.KEY_GO_LEFT)
            elif option[0] == OptionKey.KEY_GO_RIGHT:
                self.__buttons.append(Button(chr(option[1]), text_size, (x_column2 * surface.get_size()[0], (optionsY + 1 * options_y_offset) * surface.get_size()[1]), True, Command.OPTIONS_CHANGE_KEY))
                self._controls.append(self.__buttons[-1])
                self.__buttons_optionKeys.append(OptionKey.KEY_GO_RIGHT)
            elif option[0] == OptionKey.KEY_JUMP:
                self.__buttons.append(Button(chr(option[1]), text_size, (x_column2 * surface.get_size()[0], (optionsY + 2 * options_y_offset) * surface.get_size()[1]), True, Command.OPTIONS_CHANGE_KEY))
                self._controls.append(self.__buttons[-1])
                self.__buttons_optionKeys.append(OptionKey.KEY_JUMP)                
            elif option[0] == OptionKey.KEY_CROUCH:
                self.__buttons.append(Button(chr(option[1]), text_size, (x_column2 * surface.get_size()[0], (optionsY + 3 * options_y_offset) * surface.get_size()[1]), True, Command.OPTIONS_CHANGE_KEY))
                self._controls.append(self.__buttons[-1])
                self.__buttons_optionKeys.append(OptionKey.KEY_CROUCH)                
            elif option[0] == OptionKey.KEY_ATTACK:
                self.__buttons.append(Button(chr(option[1]), text_size, (x_column2 * surface.get_size()[0], (optionsY + 4 * options_y_offset) * surface.get_size()[1]), True, Command.OPTIONS_CHANGE_KEY))
                self._controls.append(self.__buttons[-1])
                self.__buttons_optionKeys.append(OptionKey.KEY_ATTACK)                
            elif option[0] == OptionKey.KEY_TELEKINESIS:
                self.__buttons.append(Button(chr(option[1]), text_size, (x_column2 * surface.get_size()[0], (optionsY + 5 * options_y_offset) * surface.get_size()[1]), True, Command.OPTIONS_CHANGE_KEY))
                self._controls.append(self.__buttons[-1])
                self.__buttons_optionKeys.append(OptionKey.KEY_TELEKINESIS)

        # kolumna 4 - slider
            elif option[0] == OptionKey.VOLUME:
                self.__sliders.append((OptionKey.VOLUME, Slider((x_column4 * surface.get_size()[0], optionsY * surface.get_size()[1]), option[1])))
            
        # kolumna 4 - rozdzielczość
        buttBox = []
        buttBox.append(Button("720x480", text_size, (0, 0), True, Command.OPTIONS_CHANGE_KEY))
        buttBox.append(Button("1280x720", text_size, (0, 0), True, Command.OPTIONS_CHANGE_KEY))
        buttBox.append(Button("xDxD", text_size, (0, 0), True, Command.OPTIONS_CHANGE_KEY))
        self._buttons_box = ButtonsBox((x_column4 * surface.get_size()[0], (optionsY + options_y_offset) * surface.get_size()[1]), buttBox)


        # tworzenie przycisków i przypisanie każdego z nich do ogólnej tablicy kontrolek
        self.__buttons.append(Button("Wyjdź", 60, (0.2 * surface.get_size()[0], 0.7 * surface.get_size()[1]), True, Command.EXIT))
        self._controls.append(self.__buttons[-1])
        self.__buttons.append(Button("Zapisz", 60, (0.4 * surface.get_size()[0], 0.7 * surface.get_size()[1]), True, Command.SAVE_OPTIONS))
        self._controls.append(self.__buttons[-1])

    def render(self):
        #zaktualizowanie stanu kontrolek (np. ich koloru)
        for control in self._controls:
            control.update()
        for slider in self.__sliders:
            slider[1].update()
        self._buttons_box.update()

        #wypełnienie ekranu kolorem
        self._surface.fill((250, 200, 190))

        #wyrysowanie wszystkich przycisków na ekran
        for butt in self.__buttons:
            butt.draw(self._surface)

        for tex in self.__texts:
            tex.draw(self._surface)

        for sli in self.__sliders:
            sli[1].draw(self._surface)

        self._buttons_box.draw(self._surface)

        #ukazanie nowej zawartości użytkownikowi
        py.display.update()

    # aktualizacja opcji
    def update_options(self):
        self.update_options_from_sliders()
        self.update_options_from_buttons()

    # aktualizacja opcji na podstawie stanu sliderów
    def update_options_from_sliders(self):
        for slide in self.__sliders:
            for option in self._options:
                # czy klucz opcji zgadza się z kluczem przypisanym sliderowi
                if option[0] == slide[0]:
                    # usuwam tuple, bo nie da się ich zmieniać
                    self._options.remove((option[0], option[1]))
                    break
            # dodaje nowy tuple do listy z odpowiednimi wartościami
            self._options.append((slide[0], slide[1].get_current_value()))

    def update_options_from_buttons(self):
        iter = 0
        for butt_key in self.__buttons_optionKeys:
            for option in self._options:
                # czy klucz opcji zgadza się z kluczem przypisanym sliderowi
                if option[0] == butt_key:
                    # usuwam tuple, bo nie da się ich zmieniać
                    self._options.remove((option[0], option[1]))
                    break
            # dodaje nowy tuple do listy z odpowiednimi wartościami
            self._options.append((butt_key, str(ord(self.__buttons[iter].get_text()))))
            iter += 1

    # gettery | settery
    def get_sliders(self):
        sliders = []
        for slide in self.__sliders:
            sliders.append(slide[1])
        return sliders

    def get_options(self):
        return self._options

    def set_options(self, new_options):
        self._options = new_options
