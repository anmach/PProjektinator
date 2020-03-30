from .gameObject import GameObject
import pygame as py

class Player(GameObject):
    """Klasa opisująca gracza."""
    def __init__(self, image_source):
        super().__init__(10, 10, 100, 100, True, image_source)
