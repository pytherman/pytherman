import esper

from components import (Velocity, Position, Renderable)


class MovementSystem(esper.Processor):
    def __init__(self, minx, maxx, miny, maxy):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

    def process(self):
        for components in self.world.get_components(Velocity, Position, Renderable):
            entity, (velocity, position, renderable) = components
            position.x += velocity.x
            position.y += velocity.y
            position.x = max(self.minx, position.x)
            position.y = max(self.miny, position.y)
            position.x = min(self.maxx - renderable.w, position.x)
            position.y = min(self.maxy - renderable.h, position.y)
