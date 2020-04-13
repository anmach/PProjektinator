from enum import IntEnum

class ObjectType(object):
    """Klasa typów obiektów w grze"""
    # obiekt nieruchomy
    STATIC = 0b0000_0000
    # obiekt ruchomy
    DYNAMIC = 0b1000_0000
    # pocisk
    BULLET = 0b000_0001



