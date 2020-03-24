from src.model.modelMenu import Model
from src.enum.command import Command
import os


#klasa reprezentująca model przeglądarki poziomów
class ModelLevelBrowser(Model):

    def __init__(self):
        super().__init__()

        #pobranie informacji o zawartości folderu
        #       v-----nie działa-----v
        _, _, fileList = os.walk('.\saves\levels')

        #trzeci element to lista plików w katalogu
        #self.__levelList = dirInfo[2]

        #nr aktualnie wybranego poziomu
        self.__shownLevel = 0

    #metoda aktualizująca stan wewnętrzego modelu programu
    def update(self):
        #wyjście do menu
        if self._command == Command.EXIT:
            self._runMode = false;

        #wybór kolejnego poziomu
        elif self._command == Command.NEXT_LEVEL and self.__levelShown < (self.__levelList) - 1:
            self.__shownLevel += 1

        #wybór poprzedniego poziomu
        elif self._command == Command.PREV_LEVEL and self.__levelShown > 0:
            self.__shownLevel -= 1

    #v----GETTERY----v
    def getShownLevelNumber(self):
        return self.__shownLevel