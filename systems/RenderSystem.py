import pygame
import esper

from components import (Position, Renderable)


class RenderSystem(esper.Processor):
    def __init__(self, screen, clear_color=(0, 0, 0)):
        super().__init__()
        self.screen = screen
        self.clear_color = clear_color

    def process(self):
        self.screen.fill(self.clear_color)
        for (entity,
             (position,
              renderable)) in self.world.get_components(Position, Renderable):
            self.screen.blit(renderable.image, (position.x, position.y))
        pygame.display.flip()
