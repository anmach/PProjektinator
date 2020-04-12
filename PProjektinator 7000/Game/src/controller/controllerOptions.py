from src.controller.controller import Controller
from src.model.modelOptions import ModelOptions
from src.view.viewOptions import ViewOptions
from src.enum.command import Command
import pygame as py

class ControllerOptions(Controller):
  #przetwarzanie danych wejściowych
    def __init__(self):
        super().__init__()
        
        # tablica sliderów
        self._sliders = []

    def process_input(self):
        for event in py.event.get():

            #naciśnięcie X okna
            if event.type == py.QUIT:
                self._command = Command.EXIT

            #kliknięcie myszką
            if event.type == py.MOUSEBUTTONDOWN:
                for control in self._controls:
                    #sprawdzanie czy nad daną kontrolką jest kursor
                    if control.get_is_focused():
                        self._command = control.get_command()
                        break
                for slider in self._sliders:
                    if slider.get_is_focused():
                        slider.move()
                        break
            else:
                self._command = Command.CONTINUE
            

    #w menu nie ma potrzeby przekazywania modelu do widoku
    def communicateMV(self, model, view):
        pass

    def get_controls(self, view):
        self._controls = view.get_controls()
        self._sliders = view.get_sliders()

    def give_command(self, model):
        model.set_command(self._command)


