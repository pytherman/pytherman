"""Explodable component"""


class Explodable(object):
    """Explodable component defines when and
       how things should explode."""

    def __init__(self, explosion_time):
        self.explosion_time = explosion_time
