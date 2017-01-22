"""Damage system"""

import random

import esper

from components import Health, Treasure
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
