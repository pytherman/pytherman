"""Treasure component"""


class Treasure:
    """Defines if entity can drop upgrade after destruction."""

    def __init__(self, chance):
        self.chance = chance
