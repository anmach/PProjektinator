from .gameObject import GameObject
from src.enum.objectType import ObjectType
import pygame as py

class Player(GameObject):
    """Klasa opisująca gracza."""
    def __init__(self, image_source):
        super().__init__(700, 20, 50, 100, True, ObjectType.DYNAMIC, image_source)

