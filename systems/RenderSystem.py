"""Render system"""

import esper
import pygame

from components import Physics

# scaling factor, from box2d world to pygame world
# for box2d, without scaling, 1 pixel is equal to 1 meter
PPM = 20.0


class RenderSystem(esper.Processor):
    """Responsible for rendering entities on screen."""

    def __init__(self, screen, clear_color=(0, 0, 0)):
        super().__init__()
        self.screen = screen
        self.clear_color = clear_color

    def process(self):
        self.screen.fill(self.clear_color)
        for _, physics in self.world.get_component(Physics):
            body = physics.body
            for fixture in body.fixtures:
                shape = fixture.shape
                vertices = [(body.transform * v) * PPM for v in shape.vertices]
                vertices = [(v[0], 480 - v[1]) for v in vertices]
                pygame.draw.polygon(self.screen,
                                    (0, 0, 255, 255),
                                    vertices)
            # self.screen.blit(renderable.image, (position.x, position.y))
        pygame.display.flip()
