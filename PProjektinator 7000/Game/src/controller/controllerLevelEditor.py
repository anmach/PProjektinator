from .controller import Controller


class ControllerLevelEditor(Controller):

    def __init__(self):
        super().__init__()

    #metoda pozwalająca pobrać kontrolki z widoku (do sprawdzenia interakcji użytkownika z nimi)
    @abstractmethod
    def get_controls(self, view):
        self._controls = view.getControls()

    #główna metoda przetwarzająca i interpretująca dane wejściowe od użytkownika
    @abstractmethod
    def process_input(self):
        pass

    #metoda pozwalająca przekazać model do widoku w celu jego wyrenderowania
    @abstractmethod
    def communicateMV(self, model, view):
        view.setModel()

    #metoda pozwalająca na przekazanie polecenia do modelu
    @abstractmethod
    def give_command(self, model):
        pass