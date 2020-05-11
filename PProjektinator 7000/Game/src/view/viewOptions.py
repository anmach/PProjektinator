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
                
        surface_size_x = surface.get_size()[0]
        surface_size_y = surface.get_size()[1]

        # rozmieszczenie po ekranie tekstu i przycisków ustawień
        small_control_size = int(0.02 * surface_size_x)
        x_column1 = 0.1
        x_column2 = 0.3
        x_column3 = 0.5
        x_column4 = 0.7
        optionsY = 0.15
        options_y_offset = 0.07
                
        big_control_size = int(0.04 * surface_size_x)

        # tworzenie wyświetlanego tekstu
        self.__texts.append(Text("Ustawienia", big_control_size, (0.35 * surface_size_x, 0.03 * surface_size_y)))

        # kolumna 1 - tekst dotyczący zmiany sterowania
        self.__texts.append(Text("Ruch w lewo", small_control_size, (x_column1 * surface_size_x, optionsY * surface_size_y)))
        self.__texts.append(Text("Ruch w prawo", small_control_size, (x_column1 * surface_size_x, (optionsY + 1 * options_y_offset) * surface_size_y)))
        self.__texts.append(Text("Skok", small_control_size, (x_column1 * surface_size_x, (optionsY + 2 * options_y_offset) * surface_size_y)))
        self.__texts.append(Text("Kucnięcie", small_control_size, (x_column1 * surface_size_x, (optionsY + 3 * options_y_offset) * surface_size_y)))
        self.__texts.append(Text("Atak", small_control_size, (x_column1 * surface_size_x, (optionsY + 4 * options_y_offset) * surface_size_y)))
        self.__texts.append(Text("Telekineza", small_control_size, (x_column1 * surface_size_x, (optionsY + 5 * options_y_offset) * surface_size_y)))
        
        # kolumna 3 - tekst
        self.__texts.append(Text("Głośność", small_control_size, (x_column3 * surface_size_x, (optionsY) * surface_size_y)))
        self.__texts.append(Text("Rozdzielczość", small_control_size, (x_column3 * surface_size_x, (optionsY + options_y_offset) * surface_size_y)))
        
        # kolumna 2 - przyciski do zmiany sterowania
        for option in self._options:
            if option[0] == OptionKey.KEY_GO_LEFT:
                self.__buttons.append(Button(chr(option[1]), small_control_size, (x_column2 * surface_size_x, optionsY * surface_size_y), True, Command.OPTIONS_CHANGE_KEY))
                self._controls.append(self.__buttons[-1])
                self.__buttons_optionKeys.append(OptionKey.KEY_GO_LEFT)
            elif option[0] == OptionKey.KEY_GO_RIGHT:
                self.__buttons.append(Button(chr(option[1]), small_control_size, (x_column2 * surface_size_x, (optionsY + 1 * options_y_offset) * surface_size_y), True, Command.OPTIONS_CHANGE_KEY))
                self._controls.append(self.__buttons[-1])
                self.__buttons_optionKeys.append(OptionKey.KEY_GO_RIGHT)
            elif option[0] == OptionKey.KEY_JUMP:
                self.__buttons.append(Button(chr(option[1]), small_control_size, (x_column2 * surface_size_x, (optionsY + 2 * options_y_offset) * surface_size_y), True, Command.OPTIONS_CHANGE_KEY))
                self._controls.append(self.__buttons[-1])
                self.__buttons_optionKeys.append(OptionKey.KEY_JUMP)                
            elif option[0] == OptionKey.KEY_CROUCH:
                self.__buttons.append(Button(chr(option[1]), small_control_size, (x_column2 * surface_size_x, (optionsY + 3 * options_y_offset) * surface_size_y), True, Command.OPTIONS_CHANGE_KEY))
                self._controls.append(self.__buttons[-1])
                self.__buttons_optionKeys.append(OptionKey.KEY_CROUCH)                
            elif option[0] == OptionKey.KEY_ATTACK:
                self.__buttons.append(Button(chr(option[1]), small_control_size, (x_column2 * surface_size_x, (optionsY + 4 * options_y_offset) * surface_size_y), True, Command.OPTIONS_CHANGE_KEY))
                self._controls.append(self.__buttons[-1])
                self.__buttons_optionKeys.append(OptionKey.KEY_ATTACK)                
            elif option[0] == OptionKey.KEY_TELEKINESIS:
                self.__buttons.append(Button(chr(option[1]), small_control_size, (x_column2 * surface_size_x, (optionsY + 5 * options_y_offset) * surface_size_y), True, Command.OPTIONS_CHANGE_KEY))
                self._controls.append(self.__buttons[-1])
                self.__buttons_optionKeys.append(OptionKey.KEY_TELEKINESIS)

        # kolumna 4 - slider
            elif option[0] == OptionKey.VOLUME:
                self.__sliders.append((OptionKey.VOLUME, Slider((x_column4 * surface_size_x, optionsY * surface_size_y), option[1], bar_size = (0.25 * surface_size_x, 0.04 * surface_size_y))))
            
        # kolumna 4 - rozdzielczość
            elif option[0] == OptionKey.WINDOW_HEIGHT:
                height = option[1]
            elif option[0] == OptionKey.WINDOW_WIDTH:
                width = option[1]
        buttBox = []
        index_button_chosen = 0
        buttBox.append(Button("720x480", small_control_size, (0, 0), True, Command.CHANGE_BUTTONS_BOX))
        self._controls.append(buttBox[-1])
        buttBox.append(Button("1280x720", small_control_size, (0, 0), True, Command.CHANGE_BUTTONS_BOX))
        if width == 1280 and height == 720:
            index_button_chosen = 1
        self._controls.append(buttBox[-1])
        buttBox.append(Button("600x500", small_control_size, (0, 0), True, Command.CHANGE_BUTTONS_BOX))
        if width == 600 and height == 500:
            index_button_chosen = 2
        self._controls.append(buttBox[-1])
        self._buttons_box = ButtonsBox((x_column4 * surface_size_x, (optionsY + options_y_offset) * surface_size_y), buttBox, index_button_chosen)


        # tworzenie przycisków i przypisanie każdego z nich do ogólnej tablicy kontrolek
        self.__buttons.append(Button("Wyjdź", big_control_size, (0.2 * surface_size_x, 0.7 * surface_size_y), True, Command.EXIT))
        self._controls.append(self.__buttons[-1])
        self.__buttons.append(Button("Zapisz", big_control_size, (0.4 * surface_size_x, 0.7 * surface_size_y), True, Command.SAVE_OPTIONS))
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
        self.update_options_from_buttonsBox()

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
                # czy klucz opcji zgadza się z kluczem przypisanym przyciskowi
                if option[0] == butt_key:
                    # usuwam tuple, bo nie da się ich zmieniać
                    self._options.remove((option[0], option[1]))
                    break
            # dodaje nowy tuple do listy z odpowiednimi wartościami
            self._options.append((butt_key, str(ord(self.__buttons[iter].get_text()))))
            iter += 1

    def update_options_from_buttonsBox(self):
        #w buttonBox mamy tylko rozdzielczość, więc to sprawdzamy

        #zdobywamy aktualnie ustawione wartości rozdzielczości:
        width = 1000
        height = 700
        button_text = self._buttons_box.get_button_chosen().get_text()
        if button_text == "1280x720":
            width = 1280
            height = 720
        elif button_text == "600x500":
            width = 600
            height = 500
        elif button_text == "720x480":
            width = 720
            height = 480

        #usuwamy stare i zapisujemy nowe opcje
        for option in self._options:
                # czy klucz opcji zgadza się z kluczem przypisanym szerokości/wysokości ekranu
                if option[0] == OptionKey.WINDOW_HEIGHT:
                    # usuwam tuple, bo nie da się ich zmieniać
                    self._options.remove((option[0], option[1]))
                elif option[0] == OptionKey.WINDOW_WIDTH:
                    # usuwam tuple, bo nie da się ich zmieniać
                    self._options.remove((option[0], option[1]))
        
        self._options.append((OptionKey.WINDOW_HEIGHT, str(height)))
        self._options.append((OptionKey.WINDOW_WIDTH, str(width)))


    # gettery | settery
    def get_sliders(self):
        sliders = []
        for slide in self.__sliders:
            sliders.append(slide[1])
        return sliders

    def get_buttons_box(self):
        return self._buttons_box

    def get_options(self):
        return self._options

    def set_options(self, new_options):
        self._options = new_options
