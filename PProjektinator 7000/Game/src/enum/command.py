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

    #polecenie do rozpoczęcia gry na jednym z poziomów
    PLAY = 6

    #POLECENIA DO STEROWANIA NA POZIOMIE POZIOMU
    #polecenie do skoku
    JUMP = 20

    #polecenie do podwójnego skoku
    DOUBLE_JUMP = 21

    #polecenie do ruchu w prawo
    GO_RIGHT = 22

    #polecenie do ruchu w lewo
    GO_LEFT = 23

    #polecenie do kucnięcia
    CROUCH = 24

    #polecenie do ataku wrogich jednostek
    ATTACK = 25
    
    #polecenie do złapania obiektu do poruszania siłą umysłu
    TELEKINESIS = 26