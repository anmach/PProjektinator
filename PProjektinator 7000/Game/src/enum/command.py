from enum import IntEnum


class Command(IntEnum):
    """klasa poleceń wydawanych modelowi przez kontroler"""

    #polecenie do kontynuowania pracy
    CONTINUE = 0x81,

    #polecenie do zakończenia działania danego trybu gry (wyjście z edytora, zakończenie gry itp.)
    EXIT = 0x82,

    #polecenie do przejścia do przeglądarki poziomów (z menu)
    BROWSE_LVL = 0x83,

    #polecenie do wybrania następnego dostępnego poziomu
    NEXT_LEVEL = 0x84,

    #polecenie do wybrania poprzedniego dostępnego poziomu
    PREV_LEVEL = 0x85,

    #polecenie do rozpoczęcia gry na jednym z poziomów
    PLAY = 0x86,

    #polecenie do przejścia do edytora poziomów
    EDIT = 0x87,

    #polecenie do utworzenia nowego poziomu
    CREATE_NEW = 0x88,

    #polecenie do wczytania poziomu
    OPEN = 0x89,

    #polecenie do zapisania aktualnie modyfikowanego poziomu
    SAVE = 0x90,

    #polecenie do wykonania odpowiedniej akcji na polu edycyjnym przypisanej do LPM
    CLICKED_LMB = 0x91,

    #polecenie do wykonanie odpowiedniej akcji na polu edycyjnym przeypisanej do PPM
    CLICKED_RMB = 0x92,

    #polecenie do wybrania nowego obiektu w edytorze
    OBJECT_SELECTED = 0x93,

    #polecenie do przejścia w tryb przenoszenia obiektóws
    RELOCATE_OBJECT = 0x94,

    #polecenie do przejścia w tryb usuwania obiektów
    DELETE_OBJECT = 0x95,

    #polecenie do przejścia do przodu w liście obiektów
    NEXT_OBJECTS = 0x96,

    #polecenie do przejścia do tyłu w liście obiektów
    PREV_OBJECTS = 0x97,

    #polecenie do przejścia do menu opcji
    OPTIONS = 0x100,

    # polecenie odczytania pliku opcji
    READ_OPTIONS = 0x101,

    # polecenie zapisu do pliku
    SAVE_OPTIONS = 0x102

    # polecenie zmiany klawisza sterującego w opcjach
    OPTIONS_CHANGE_KEY = 0x103

    #polecenie zmiany odczytu z ButtonsBox...
    CHANGE_BUTTONS_BOX = 0x104

    #POLECENIA DO STEROWANIA NA POZIOMIE POZIOMU
    #polecenie do skoku
    JUMP = 0b1,

    #polecenie do ruchu w górę - telekineza
    GO_UP = 0b10,

    #polecenie do ruchu w prawo
    GO_RIGHT = 0b100,

    #polecenie do ruchu w lewo
    GO_LEFT = 0b1_000,

    #polecenie do kucnięcia
    CROUCH = 0b10_000,

    #polecenie do ataku wrogich jednostek
    ATTACK = 0b100_000,
    
    #polecenie do złapania obiektu do poruszania siłą umysłu
    TELEKINESIS = 0b1_000_000,

    #polecenie pauzy - zdeterminować czy pasuje tu czy do ogólnych poleceń
    PAUSE = 0b100_000_000

