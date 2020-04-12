from enum import IntEnum


class EditingMode(IntEnum):
    #kliknięcie myszką na ekran edycji nic nie zdziała
    NONE = 0,

    #tworzenie platformy
    PLATFORM_CREATION = 1,

    #wstawianie nowego obiektu
    OBJECT_PLACEMENT = 2
