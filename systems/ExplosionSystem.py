"""Explosion system"""

import esper
import time
import math
import Box2D
import pygame

from components import Physics, Explodable, Renderable
from messaging import DamageMessage
from Box2D.b2 import vec2


NUM_RAYS = 64
BLAST_RADIUS = 2
BLAST_POWER = 1000
BLAST_DAMAGE = 1


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
                        # force = callback.point - physics.body.position
                        # force.Normalize()
                        # callback.fixture.body.ApplyForce(force=force * BLAST_POWER,
                        #                                  point=callback.point,
                        #                                  wake=True)
                        self.world.msg_bus.add(DamageMessage(entity, callback.fixture.body.userData, BLAST_DAMAGE))
                explosion_image = pygame.image.load("assets/explosion.png")
                explosion = self.world.create_entity()
                explosion_body = self.world.pworld.CreateStaticBody(position=physics.body.position)
                self.world.add_component(explosion, Renderable(image=explosion_image))
                self.world.add_component(explosion, Physics(body=explosion_body))
                self.world.pworld.DestroyBody(physics.body)
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
        return -1
