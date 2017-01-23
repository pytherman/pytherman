"""System responsible for executing actions such as planting bomb."""

import time

import esper
import pygame

from components import Bomber, Explodable, Physics, Renderable
from messaging import Intent, MessageType


class ActionSystem(esper.Processor):
    """Responsible for executing actions."""

    def __init__(self):
        super().__init__()

    def process(self):
        for intent in self.world.msg_bus.get_by_type(MessageType.INTENT):
            if intent.intent == Intent.PLANT_BOMB:
                bomber = self.world.component_for_entity(intent.source,
                                                         Bomber)
                source_physics = self.world.component_for_entity(intent.source,
                                                                 Physics)
                if bomber.used < bomber.max:
                    if time.time() > bomber.last_planted + bomber.cooldown:
                        self._spawn_bomb(intent.source, source_physics)
                        bomber.last_planted = time.time()
                        bomber.used += 1
                        print("cokolwiek")

    def _spawn_bomb(self, source, source_physics):
        bomb = self.world.create_entity()
        bomb_image = pygame.image.load("assets/tnt_barrel.png")
        bomb_renderable = Renderable(image=bomb_image)
        bomb_body = self.world.pworld.CreateDynamicBody(
            position=source_physics.body.position)
        bomb_body.CreatePolygonFixture(
            box=(bomb_renderable.w / self.world.PPM / 2,
                 bomb_renderable.h / self.world.PPM / 2),
            density=1,
            friction=0.3)
        # TODO
        # For now bomb physics is disabled, need to implement collision
        # listener and filter in PreSolve and mark bomb as "clean"
        # after first contact with source ended (EndContact)
        bomb_body.active = False
        self.world.add_component(bomb, Physics(body=bomb_body))
        self.world.add_component(bomb, bomb_renderable)
        self.world.add_component(bomb,
                                 Explodable(explosion_time=time.time() + 1, planter=source))
