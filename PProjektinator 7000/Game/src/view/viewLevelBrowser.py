from .view import View


class ViewLevelBrowser(View):

    def __init__(self, surface):
        super().__init__(surface)

        #tablica przycisków
        self.__buttons = []

        #tworzenie przycisków i przypisanie każdego z nich do ogólnej tablicy kontrolek
        self.__buttons.append(Button("Wyjdz", 50, (0.4 * surface.get_size()[0], 0.8 * surface.get_size()[1]), True, Command.EXIT))
        self._controls.append(self.__buttons[-1])

    #metoda renderująca
    @abstractmethod
    def render(self):
        pass
    
    #metoda pozwalająca na pobranie modelu (może się różnic dla każdego z trybów programu)
    @abstractmethod
    def setModel(self):
        pass