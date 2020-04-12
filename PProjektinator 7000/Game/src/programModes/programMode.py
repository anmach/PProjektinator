from abc import ABC, abstractmethod
from src.model.model import Model
from src.view.view import View
from src.controller.controller import Controller
import pygame as py


class ProgramMode(ABC):
    """klasa bazowa trybów programu takich jak Menu, Edytor poziomów, Gra"""

    runMode = True

    def __init__(self):
        self._model = Model()
        self._view = View()
        self._controller = Controller()
    
    
    def run(self):
        #główne pętla aktualnego trybu programu
        while self._model.get_run_mode():
            if(self._model.get_change_mode()):
                self.change_mode()
            
            #przetwarzanie danych wejściowych
            self.process_input()

            #aktualizacja stanu modelu
            self.update()

            #renderowanie
            self.render()

            #ograniczenie fps?
            clock = py.time.Clock()
            clock.tick(60)

    #metoda tworząca odpowiedni nowy tryb i uruchamiająca go
    @abstractmethod
    def change_mode(self):
        pass

    #metoda, która zajmuje się wszelkimi rzeczami związanymi z danymi wejściowymi od użytkownika
    #@abstractmethod
    def process_input(self):
        self._controller.get_controls(self._view)
        self._controller.process_input()

    #metoda, która zajmuje się wszelkimi rzeczami związanymi z aktualizowaniem stanu wewnętrzego modelu
    #@abstractmethods
    def update(self):
        self._controller.give_command(self._model)
        self._model.update()

    #metoda, która zajmuje się wszelkimi rzeczami związanymi z renderowaniem obiektów na ekran
    #@abstractmethod
    def render(self):
        self._controller.communicateMV(self._model, self._view)
        self._view.render()
