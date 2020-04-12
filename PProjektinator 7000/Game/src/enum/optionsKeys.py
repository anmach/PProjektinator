from enum import IntEnum

class optionsKeys(IntEnum):
    """ Klasa z kluczami/nazwami opcji do ustawiania w menu opcji.
        Przydatne przy zapisie opcji do pliku czy ustawianiu nowych klawiszy
    """

    KEY_GO_LEFT = 1
    KEY_GO_RIGHT = 2
    KEY_JUMP = 3

    VOLUME = 20
    WINDOW_WIDTH = 21
    WINDOW_HEIGHT = 22

