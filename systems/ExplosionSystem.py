"""Explosion system"""

import esper
import time

from components import Physics, Explodable


class ExplosionSystem(esper.Processor):
    """Responsible for exploding things up."""

    def __init__(self):
        super().__init__()

    def process(self):
        for (entity, (physics,
                      explodable)) in self.world.get_components(Physics,
                                                                Explodable):
            if explodable.explosion_time < time.time():
                self.world.delete_entity(entity)
