from enum import IntEnum

class ObjectType(IntEnum):
    """Enum typów obiektów w grze"""
    # przeszkoda (cały jej rozmiar ma kolizje - nie da się wskoczyć od dołu)
    STATIC = 1,
    # skrzynie
    DYNAMIC = 2,
    # pocisk
    BULLET = 3,
    # ruchoma platforma
    KINEMATIC = 4,
    # postać 
    PLAYER = 5
    # wrogowie
    ENEMY = 6,
    # zakończenie poziomu - meta
    FINISH_LINE = 7

