from .view import View


class ViewLevelEditor(View):

    def __init__(self, surface):
        super().__init__(surface)

        #nr aktualnie wybranego, edytowanego poziomu
        self.__chosenLevel = -1

        #wyświetlany nr poziomu do edycji
        self.__levelToEdit = 0

        #współrzędne punktów nowej platformy
        self.__newPlatformPoints = []
