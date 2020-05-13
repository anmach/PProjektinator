from enum import IntEnum


class EditingMode(IntEnum):
    """Enum określający tryb pracy edytora."""

    #kliknięcie myszką na ekran edycji nic nie zdziała
    NONE = 0,

    #tworzenie platformy
    PLATFORM_CREATION = 1,

    #wstawianie gracza
    PLAYER_PLACEMENT = 2,

    #wstawianie skrzyni
    CRATE_PLACEMENT = 3,

    #wstawianie ruchomej platformy
    MOVING_PLATFORM_PLACEMENT = 4,

    #przenoszenie obiektów
    OBJECT_RELOCATION = 30,

    #usuwanie obiektów
    DELETION = 40
