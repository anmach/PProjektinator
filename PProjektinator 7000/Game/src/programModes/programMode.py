from abc import ABC, abstractmethod
from src.model.model import Model
from src.view.view import View
from src.controller.controller import Controller


#klasa bazowa trybów programu takich jak Menu, Edytor poziomów, Gra
class ProgramMode(ABC):

    runMode = True

    def __init__(self):
        self._model = Model()
        self._view = View()
        self._controller = Controller()
    
    
    def run(self):
        #główne pętla aktualnego trybu programu
        while self._model.getRunMode() :
            if(self._model.getChangeMode())
                self.changeMode()
            
            #przetwarzanie danych wejściowych
            self.processInput()

            #aktualizacja stanu modelu
            self.update()

            #renderowanie
            self.render()


    @abstractmethod
    def changeMode(self):
        pass

    #metoda, która zajmuje się wszelkimi rzeczami związanymi z danymi wejściowymi od użytkownika
    #@abstractmethod
    def processInput(self):
        self._controller.getControls(self._view)
        self._controller.processInput()

    #metoda, która zajmuje się wszelkimi rzeczami związanymi z aktualizowaniem stanu wewnętrzego modelu
    #@abstractmethods
    def update(self):
        self._controller.giveCommand(self._model)
        self._model.update()

    #metoda, która zajmuje się wszelkimi rzeczami związanymi z renderowaniem obiektów na ekran
    #@abstractmethod
    def render(self):
        self._controller.communicateMV(self._model, self._view)
        self._view.render()