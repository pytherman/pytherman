"""Movement system"""

import esper

from components import Physics, Velocity
from messaging import Intent, MessageType


class MovementSystem(esper.Processor):
    """Responsible for moving entities."""

    def __init__(self):
        super().__init__()

    def process(self):
        for intent in self.world.msg_bus.get_by_type(MessageType.INTENT):
            if intent.intent == Intent.MOVE_LEFT:
                velocity = self.world.component_for_entity(intent.source,
                                                           Velocity)
                velocity.x = -1 * velocity.value
            elif intent.intent == Intent.MOVE_RIGHT:
                velocity = self.world.component_for_entity(intent.source,
                                                           Velocity)
                velocity.x = velocity.value
            elif intent.intent == Intent.MOVE_UP:
                velocity = self.world.component_for_entity(intent.source,
                                                           Velocity)
                velocity.y = velocity.value
            elif intent.intent == Intent.MOVE_DOWN:
                velocity = self.world.component_for_entity(intent.source,
                                                           Velocity)
                velocity.y = -1 * velocity.value
            elif intent.intent == Intent.MOVE_CLEAR_HORIZONTAL:
                self.world.component_for_entity(intent.source,
                                                Velocity).x = 0
            elif intent.intent == Intent.MOVE_CLEAR_VERTICAL:
                self.world.component_for_entity(intent.source,
                                                Velocity).y = 0

        for (_, (velocity,
                 physics)) in self.world.get_components(Velocity, Physics):
            physics.body.linearVelocity = (velocity.x, velocity.y)
