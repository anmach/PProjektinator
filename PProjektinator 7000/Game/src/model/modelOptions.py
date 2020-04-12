from src.model.model import Model
from src.enum.command import Command

class ModelOptions(Model):
    """klasa reprezentująca model menu opcji"""

    def __init__(self):
        super().__init__()
        self.__options_file_name = '.\\saves\\opszyns.txt'

        # stworzenie tablicy z opcjami -- tablica[x] = (optionKey, wartość)
        self._options = []
        self.read_options_file()
    
    # odczyt pliku z zapisanymi opcjami
    def read_options_file(self):    
        file = open(self.__options_file_name)
        
        # odczyt kolejnych linii
        for line in file:
            splitted_line = line.strip().split()
            # dodanie informacji do tablicy opcji
            self._options.append((splitted_line[0], splitted_line[1]))

        file.close()

    # zapis ustawień do pliku
    def save_to_options_file(self):
        file = open(self.__options_file_name, 'w')
        
        for option in self._options:
            file.write(option[0])
            file.write(' ')
            file.write(option[1])

        file.close()

    def update(self):
        if self._command == Command.EXIT:
            self._runMode = False

    # gettery | settery
    def get_options(self):
        return self._options

    def set_options(self, new_options):
        self._options = new_options

