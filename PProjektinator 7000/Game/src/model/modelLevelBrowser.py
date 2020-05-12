from src.model.modelMenu import Model
from src.enum.command import Command
import os
import src.define as define

class ModelLevelBrowser(Model):
    """klasa reprezentująca model przeglądarki poziomów"""

    def __init__(self):
        super().__init__()

        #pobranie informacji o zawartości folderu
        #       v-----inaczej nie działa-----v
        for (_, _, fileList) in os.walk(define.get_levels_folder_path()):
            self.__levelList = fileList

        #nr aktualnie wybranego poziomu
        self.__shownLevel = 0

    #metoda aktualizująca stan wewnętrzego modelu programu
    def update(self):
        #wyjście do menu
        if self._command == Command.EXIT:
            self._runMode = False

        #wybór kolejnego poziomu
        elif self._command == Command.NEXT_LEVEL and self.__shownLevel < (len(self.__levelList)) - 1:
            self.__shownLevel += 1

        #wybór poprzedniego poziomu
        elif self._command == Command.PREV_LEVEL and self.__shownLevel > 0:
            self.__shownLevel -= 1

        elif self._command == Command.PLAY:
            print("Rozpoczęto grę na poziomie " + str(self.__shownLevel))
            self._changeMode = True

    #v----GETTERY----v
    def get_shown_level_number(self):
        return self.__shownLevel
