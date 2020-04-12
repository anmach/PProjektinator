from src.controller.controller import Controller
from src.model.modelOptions import ModelOptions
from src.view.viewOptions import ViewOptions
from src.enum.command import Command
import pygame as py

class ControllerOptions(Controller):
  #przetwarzanie danych wejściowych
    def __init__(self):
        super().__init__()

        self._is_mouse_pressed = 0
        
        # tablica sliderów
        self._sliders = []

    def process_input(self):
        if self._is_mouse_pressed == 0:
            for event in py.event.get():
                #naciśnięcie X okna
                if event.type == py.QUIT:
                    self._command = Command.EXIT

                # kliknięcie myszką
                if event.type == py.MOUSEBUTTONDOWN:
                    for control in self._controls:
                        # sprawdzanie czy nad daną kontrolką jest kursor
                        if control.get_is_focused():
                            self._command = control.get_command()
                            break
                    for slider in self._sliders:
                        #sprawdzenie czy nad sliderem jest kursor
                        if slider.get_is_focused():
                            self._is_mouse_pressed = 1
                            slider.set_is_pushed(1)
                            slider.move()
                            break
                else:
                    self._command = Command.CONTINUE
        else:    
            # poruszanie slidera
            for slider in self._sliders:
                if slider.get_is_focused():
                    slider.move()
                    break 
            for event in py.event.get():
                # koniec nacisku myszy
                if event.type == py.MOUSEBUTTONUP:
                    self._is_mouse_pressed = 0
                    # zresetowanie sliderów jako nienaciśnięte
                    for slider in self._sliders:
                        slider.set_is_pushed(0)
               
    # w menu nie ma potrzeby przekazywania modelu do widoku
    def communicateMV(self, model, view):
        pass

    def get_controls(self, view):
        self._controls = view.get_controls()
        self._sliders = view.get_sliders()

    def give_command(self, model):
        model.set_command(self._command)


