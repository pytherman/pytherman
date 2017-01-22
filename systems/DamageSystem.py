"""Damage system"""

import esper

from components import Health, Physics
from messaging import MessageType


class DamageSystem(esper.Processor):
    """Responsible for moving entities."""

    def __init__(self):
        super().__init__()

    def process(self):
        for damage in self.world.msg_bus.get_by_type(MessageType.DAMAGE):
            try:
                target_hp = self.world.component_for_entity(damage.target, Health)
                if target_hp:
                    target_hp.hp -= damage.damage
                    if target_hp.hp <= 0:
                        target_physics = self.world.component_for_entity(damage.target, Physics)
                        if target_physics.body:
                            self.world.pworld.DestroyBody(target_physics.body)
                            target_physics.body = None
                        self.world.delete_entity(damage.target)
            except KeyError:
                pass
