from src.model.model import Model
from src.enum.command import Command

class ModelOptions(Model):
    """klasa reprezentująca model menu opcji"""

    def __init__(self):
        super().__init__()

        # stworzenie tablicy z opcjami -- tablica[x] = (klucz, wartość)
        self._options = []
        self.read_options_file()
    
    # odczyt pliku z zapisanymi opcjami
    def read_options_file(self):    
        file = open('.\\saves\\opszyns.txt')
        
        # odczyt kolejnych linii
        for line in file:
            splitted_line = line.strip().split()
            # dodanie informacji do tablicy opcji
            self._options.append((splitted_line[0], splitted_line[1]))

        file.close()

    def update(self):
        if self._command == Command.EXIT:
            self._runMode = False

    # gettery | settery
    def get_options(self):
        return self._options

