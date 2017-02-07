"""Class woth basic artificial intelligence for enemy in game"""
import random
import esper
import math

import Box2D
from Box2D.b2 import vec2
from components import AIControllable, Physics, Explodable, Health
from components import Bomber
from components import Velocity
from systems.ExplosionSystem import RayCastClosestCallback
from messaging import IntentMessage, Intent


class AISystem(esper.Processor):
    """class with behaiour of enemy"""

    def __init__(self):
        super().__init__()
        self.move_handler = self.dummy_ai

    def dummy_ai(self, entity):
        """basic dummy ai - move inn random direction, plant bomb in random time"""
        arr = [Intent.MOVE_LEFT, Intent.MOVE_RIGHT, Intent.MOVE_UP, Intent.MOVE_DOWN, Intent.PLANT_BOMB]
        self.world.msg_bus.add(IntentMessage(entity, arr[random.randint(0, 4)]))

    def smarter_ai(self, entity):
        """a little smarter ai - move randomly but plant bomb only if is close to something destroyable"""
        velocity = self.world.component_for_entity(entity, Velocity)
        velocity.value = 10
        arr = [Intent.MOVE_LEFT, Intent.MOVE_RIGHT, Intent.MOVE_UP, Intent.MOVE_DOWN, Intent.PLANT_BOMB]
        destroyable = self._get_in_range(entity, Health)
        (closest, dist, v_x, v_y) = self._get_closest(entity, destroyable)
        if dist < 2:
            self.world.msg_bus.add(IntentMessage(entity, Intent.PLANT_BOMB))
        else:
            self.world.msg_bus.add(IntentMessage(entity, arr[random.randint(0, 3)]))

    def smarter_and_faster_ai(self, entity):
        """ai is faster then the dummy one and enemy is twice faster then them"""
        velocity = self.world.component_for_entity(entity, Velocity)
        velocity.value = 20
        arr = [Intent.MOVE_LEFT, Intent.MOVE_RIGHT, Intent.MOVE_UP, Intent.MOVE_DOWN, Intent.PLANT_BOMB]
        destroyable = self._get_in_range(entity, Health)
        (closest, dist, v_x, v_y) = self._get_closest(entity, destroyable)
        if dist < 2:
            self.world.msg_bus.add(IntentMessage(entity, Intent.PLANT_BOMB))
        else:
            self.world.msg_bus.add(IntentMessage(entity, arr[random.randint(0, 3)]))

    def smarter_faster_and_run_away_for_bombs_ai(self, entity):
        """ai check if bomb is planted close to enemy and run away"""
        velocity = self.world.component_for_entity(entity, Velocity)
        velocity.value = 20
        arr = [Intent.MOVE_LEFT, Intent.MOVE_RIGHT, Intent.MOVE_UP, Intent.MOVE_DOWN, Intent.PLANT_BOMB]
        bombs = self._get_in_range(entity, Explodable)
        (closest, dist, v_x, v_y) = self._get_closest(entity, bombs)
        if dist < 2:
            if v_x > 0:
                self.world.msg_bus.add(IntentMessage(entity,
                                                     Intent.MOVE_LEFT))
            else:
                self.world.msg_bus.add(IntentMessage(entity,
                                                     Intent.MOVE_RIGHT))
            if v_y > 0:
                self.world.msg_bus.add(IntentMessage(entity,
                                                     Intent.MOVE_DOWN))
            else:
                self.world.msg_bus.add(IntentMessage(entity,
                                                     Intent.MOVE_UP))
        else:
            destroyable = self._get_in_range(entity, Health)
            (closest, dist, v_x, v_y) = self._get_closest(entity, destroyable)
            if dist < 2:
                self.world.msg_bus.add(IntentMessage(entity, Intent.PLANT_BOMB))
            else:
                self.world.msg_bus.add(IntentMessage(entity, arr[random.randint(0, 3)]))

    def smarter_faster_run_away_for_bombs_and_having_bigger_range_of_bombs_ai(self, entity):
        """ai has bigger range of bombs"""
        velocity = self.world.component_for_entity(entity, Velocity)
        velocity.value = 20
        bomber = self.world.component_for_entity(entity, Bomber)
        bomber.bombrange = 'lg'
        arr = [Intent.MOVE_LEFT, Intent.MOVE_RIGHT, Intent.MOVE_UP, Intent.MOVE_DOWN, Intent.PLANT_BOMB]
        bombs = self._get_in_range(entity, Explodable)
        (closest, dist, v_x, v_y) = self._get_closest(entity, bombs)
        if dist < 2:
            if v_x > 0:
                self.world.msg_bus.add(IntentMessage(entity, Intent.MOVE_LEFT))
            else:
                self.world.msg_bus.add(IntentMessage(entity, Intent.MOVE_RIGHT))
            if v_y > 0:
                self.world.msg_bus.add(IntentMessage(entity, Intent.MOVE_DOWN))
            else:
                self.world.msg_bus.add(IntentMessage(entity, Intent.MOVE_UP))
        else:
            destroyable = self._get_in_range(entity, Health)
            (closest, dist, v_x, v_y) = self._get_closest(entity, destroyable)
            if dist < 2:
                self.world.msg_bus.add(IntentMessage(entity, Intent.PLANT_BOMB))
            else:
                self.world.msg_bus.add(IntentMessage(entity, arr[random.randint(0, 3)]))

    def process(self):
        """move of enemy"""
        if self.world.level > 8:
            self.move_handler = self.smarter_faster_run_away_for_bombs_and_having_bigger_range_of_bombs_ai
        elif self.world.level > 6:
            self.move_handler = self.smarter_faster_and_run_away_for_bombs_ai
        elif self.world.level > 4:
            self.move_handler = self.smarter_and_faster_ai
        elif self.world.level > 2:
            self.move_handler = self.smarter_ai
        else:
            self.move_handler = self.dummy_ai
        for entity, _ in self.world.get_components(AIControllable):
            self.move_handler(entity)

    def _get_in_range(self, ent, elem_type):
        """Return collection of elems of elem_type close to enemy"""
        collection = set()
        physics = self.world.component_for_entity(ent, Physics)
        NUM_RAYS = 64
        RADIUS = 5
        for i in range(NUM_RAYS):
            angle = math.radians((i / NUM_RAYS) * 360)
            ray_dir = vec2(math.sin(angle), math.cos(angle))
            ray_end = physics.body.position + RADIUS * ray_dir
            callback = RayCastClosestCallback()
            self.world.pworld.RayCast(callback, physics.body.position,
                                      ray_end)
            if callback.fixture:
                try:
                    visible_ent = callback.fixture.body.userData
                    if self.world.has_component(visible_ent, elem_type):
                        collection.add(visible_ent)
                except KeyError:
                    pass
        return collection

    def _get_closest(self, ent, collection):
        """find the closest elem to enemy from collectior"""
        physics = self.world.component_for_entity(ent, Physics)
        center = physics.body.position
        max_dist = 1e6
        closest = -1
        v_x, v_y = -1, -1
        for elem in collection:
            elem_c = self.world.component_for_entity(elem, Physics).body.position
            dist = math.sqrt(math.pow(elem_c[0] - center[0], 2) + math.pow(elem_c[1] - center[1], 2))
            if dist < max_dist:
                max_dist = dist
                closest = elem
                v_x = elem_c[0] - center[0]
                v_y = elem_c[1] - center[1]
        return (closest, max_dist, v_x, v_y)
