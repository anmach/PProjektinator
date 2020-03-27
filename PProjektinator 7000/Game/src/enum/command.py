from enum import Enum


class Command(Enum):
    """klasa poleceń wydawanych modelowi przez kontroler"""

    #polecenie do kontynuowania pracy
    CONTINUE = 1,

    #polecenie do zakończenia działania danego trybu gry (wyjście z edytora, zakończenie gry itp.)
    EXIT = 2,

    #polecenie do przejścia do przeglądarki poziomów (z menu)
    BROWSE_LVL = 3,

    #polecenie do wybrania następnego dostępnego poziomu
    NEXT_LEVEL = 4,

    #polecenie do wybrania poprzedniego dostępnego poziomu
    PREV_LEVEL = 5