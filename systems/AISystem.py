import esper
import math

import Box2D
from Box2D.b2 import vec2
from components import AIControllable, Physics, Explodable, Health
from systems.ExplosionSystem import RayCastClosestCallback
from messaging import IntentMessage, Intent


class AISystem(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        print("chuj")
        for (entity, (ai)) in self.world.get_components(AIControllable):
            bombs = self._get_in_range(entity, Explodable)
            (closest, dist, v_x, v_y) = self._get_closest(entity, bombs)
            # print("{} {} {} {}".format(closest, dist, v_x, v_y))
            if dist < 2:
                if v_x > 0:
                    self.msg_bus.add(IntentMessage(Intent.MOVE_LEFT))
                else:
                    self.msg_bus.add(IntentMessage(Intent.MOVE_RIGHT))
                if v_y > 0:
                    self.msg_bus.add(IntentMessage(Intent.MOVE_DOWN))
                else:
                    self.msg_bus.add(IntentMessage(Intent.MOVE_UP))
            destroyable = self._get_in_range(entity, Health)
            (closest, dist, v_x, v_y) = self._get_closest(entity, destroyable)
            print(dist)
            if dist < 10:
                self.msg_bus.add(IntentMessage(Intent.PLACE_BOMB))

    def _get_in_range(self, ent, elem_type):
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
                visible_ent = callback.fixture.body.userData
                if self.world.has_component(visible_ent, elem_type):
                    collection.add(visible_ent)
        return collection

    def _get_closest(self, ent, collection):
        physics = self.world.get_component_for_entity(ent, Physics)
        center = physics.body.position
        max_dist = 1e6
        closest = -1
        v_x, v_y = -1, -1
        for elem in collection:
            elem_c = self.world.get_component_for_entity(elem, Physics).body.position
            dist = math.sqrt(math.pow(elem_c[0] - center[0], 2) + math.pow(elem_c[1] - center[1], 2))
            if dist < max_dist:
                max_dist = dist
                closest = elem
                v_x = elem_c[0] - center[0]
                v_y = elem_c[1] - center[1]
        return (closest, max_dist, v_x, v_y)
