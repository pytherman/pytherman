"""Damage system"""

import random

import esper

from components import Bomber
from components import Health, Treasure
from components import Velocity
from messaging import Intent, IntentMessage, MessageType


class DamageSystem(esper.Processor):
    """Responsible for damaging entities."""

    def __init__(self):
        super().__init__()

    def process(self):
        for damage in self.world.msg_bus.get_by_type(MessageType.DAMAGE):
            self._inflict(damage)

    def _inflict(self, damage):
        try:
            target_hp = self.world.component_for_entity(damage.target, Health)
            if target_hp:
                target_hp.hp -= damage.damage
                if target_hp.hp <= 0:
                    self.world.to_delete.add(damage.target)
                    self._try_to_place_bonus(damage.target)
            target_bomber = self.world.component_for_entity(damage.target, Bomber)
            if target_bomber:
                target_bomber.bombrange = 'sm'
                target_bomber.damage = 1
            target_velocity = self.world.component_for_entity(damage.target, Velocity)
            if target_velocity:
                target_velocity.value = 20
        except KeyError:
            pass

    def _try_to_place_bonus(self, source):
        try:
            treausure = self.world.component_for_entity(source, Treasure)
            if random.random() > (1 - treausure.chance):
                self.world.msg_bus.add(IntentMessage(
                    source,
                    Intent.PLACE_BONUS))
        except KeyError:
            pass
