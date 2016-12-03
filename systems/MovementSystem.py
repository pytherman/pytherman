"""Movement system"""

import esper

from components import Physics, Velocity


class MovementSystem(esper.Processor):
    """Responsible for moving entities."""

    def __init__(self):
        super().__init__()

    def process(self):
        for (_, (velocity,
                 physics)) in self.world.get_components(Velocity, Physics):
            physics.body.linearVelocity = (velocity.x, velocity.y)
