"""Velocity component"""


class Velocity(object):
    """Velocity component allows to move entity on X and Y axes."""

    def __init__(self, x=0.0, y=0.0, value=20.0):
        self.x = x
        self.y = y
        self.value = value
