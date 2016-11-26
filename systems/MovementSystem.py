import esper

from components import Velocity, Renderable


class MovementSystem(esper.Processor):
    def __init__(self, minx, maxx, miny, maxy):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

    def process(self):
        for components in self.world.get_components(Velocity, Renderable):
            entity, (velocity, renderable) = components
            renderable.x += velocity.x
            renderable.y += velocity.y
            renderable.x = max(self.minx, renderable.x)
            renderable.y = max(self.miny, renderable.y)
            renderable.x = min(self.maxx - renderable.w, renderable.x)
            renderable.y = min(self.maxy - renderable.h, renderable.y)
