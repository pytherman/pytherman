"""Movement system"""

import esper

from components import Physics, Velocity
from messaging import MessageType, Intent


class MovementSystem(esper.Processor):
    """Responsible for moving entities."""

    def __init__(self):
        super().__init__()

    def process(self):
        player_velocity = self.world.component_for_entity(self.world.player,
                                                          Velocity)
        for intent in self.world.msg_bus.get_by_type(MessageType.INTENT):
            if intent.intent == Intent.MOVE_LEFT:
                player_velocity.x = -10
            elif intent.intent == Intent.MOVE_RIGHT:
                player_velocity.x = 10
            elif intent.intent == Intent.MOVE_UP:
                player_velocity.y = 10
            elif intent.intent == Intent.MOVE_DOWN:
                player_velocity.y = -10
            elif intent.intent == Intent.MOVE_CLEAR_HORIZONTAL:
                player_velocity.x = 0
            elif intent.intent == Intent.MOVE_CLEAR_VERTICAL:
                player_velocity.y = 0

        for (_, (velocity,
                 physics)) in self.world.get_components(Velocity, Physics):
            physics.body.linearVelocity = (velocity.x, velocity.y)
