from src.model.model import Model
from src.enum.command import Command
import src.define as define

class ModelOptions(Model):
    """klasa reprezentująca model menu opcji"""

    def __init__(self):
        super().__init__()
        self.__options_file_name = define.get_options_file_path()

        # stworzenie tablicy z opcjami -- tablica[x] = (optionKey, wartość)
        self._options = []
        self.read_options_file()
    
    # odczyt pliku z zapisanymi opcjami
    def read_options_file(self):    
        file = open(self.__options_file_name, 'r')
        
        # odczyt kolejnych linii
        for line in file:
            splitted_line = line.strip().split()
            # dodanie informacji do tablicy opcji
            self._options.append((int(splitted_line[0]), int(splitted_line[1])))

        file.close()

    # zapis ustawień do pliku
    def save_to_options_file(self):
        file = open(self.__options_file_name, 'w')
        file.truncate(0)

        for option in self._options:
            file.write(str(int(option[0])))
            file.write(' ')
            file.write(str(option[1]))
            file.write('\n')

        file.close()

    def update(self):
        if self._command == Command.EXIT:
            self._runMode = False

    # gettery | settery
    def get_options(self):
        return self._options

    def set_options(self, new_options):
        self._options = new_options

