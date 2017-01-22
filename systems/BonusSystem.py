"""Bonus system"""

import random

import esper
import pygame

from components import Bomber, Bonus, Health, Physics, Renderable
from messaging import Intent, MessageType


class BonusSystem(esper.Processor):
    """Responsible for spawning bonuses."""

    def __init__(self):
        super().__init__()
        self.bonuses = [
            (_increase_hp,
             pygame.image.load("assets/bonus/hp.png")),
            (_increase_max_bomb_number,
             pygame.image.load("assets/bonus/bomb.png"))
        ]

    def process(self):
        for msg in self.world.msg_bus.get_by_type(MessageType.INTENT):
            if msg.intent == Intent.PLACE_BONUS:
                selected = random.choice(self.bonuses)
                source_pos = self.world.component_for_entity(
                    msg.source,
                    Physics).body.position
                bonus = self.world.create_entity()
                bonus_body = self.world.pworld.CreateStaticBody(
                    position=source_pos)
                self.world.add_component(bonus, Bonus(on_pickup=selected[0]))
                self.world.add_component(bonus, Renderable(image=selected[1]))
                self.world.add_component(bonus, Physics(body=bonus_body))


def _increase_hp(world, entity):
    health = world.get_component(entity, Health)
    health.hp += 1


def _increase_max_bomb_number(world, entity):
    bomber = world.get_component(entity, Bomber)
    bomber.max += 1
