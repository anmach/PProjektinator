from .gameObject import GameObject
import pygame as py

class Player(GameObject):
    """Klasa opisująca gracza."""
    def __init__(self, image_source):
        super().__init__(700, 20, 50, 50, True, True, image_source)

