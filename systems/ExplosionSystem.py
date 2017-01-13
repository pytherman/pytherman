"""Explosion system"""

import esper
import time
import math
import Box2D

from components import Physics, Explodable
from Box2D.b2 import vec2


NUM_RAYS = 32
BLAST_RADIUS = 4


class ExplosionSystem(esper.Processor):
    """Responsible for exploding things up."""

    def __init__(self):
        super().__init__()

    def process(self):
        for (entity, (physics,
                      explodable)) in self.world.get_components(Physics,
                                                                Explodable):
            if self._should_explode(explodable):
                for i in range(NUM_RAYS):
                    angle = math.radians((i / NUM_RAYS) * 360)
                    ray_dir = vec2(math.sin(angle), math.cos(angle))
                    ray_end = physics.body.position + BLAST_RADIUS * ray_dir
                    callback = RayCastClosestCallback()
                    self.world.pworld.RayCast(callback, physics.body.position,
                                              ray_end)
                    if callback.fixture:
                        callback.fixture.body.ApplyForce(force=(100000, 0),
                                                         point=callback.point,
                                                         wake=True)
                self.world.delete_entity(entity)

    def _should_explode(self, explodable):
        if explodable.explosion_time < time.time():
            return True
        return False


class RayCastClosestCallback(Box2D.b2RayCastCallback):
    """Captures the closest hit shape"""

    def __init__(self, **kwargs):
        Box2D.b2RayCastCallback.__init__(self)
        self.fixture = None

    def ReportFixture(self, fixture, point, normal, fraction):
        self.fixture = fixture
        self.point = vec2(point)
        self.normal = vec2(normal)
        # We do not want the ray to continue
        return 0
