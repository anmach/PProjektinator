from enum import Enum

#klasa poleceń wydawanych modelowi przez kontroler
class Command(Enum):

    #polecenie do kontynuowania pracy
    CONTINUE = 1,

    #polecenie do zakończenia działania danego trybu gry (wyjście z edytora, zakończenie gry itp.)
    EXIT = 2