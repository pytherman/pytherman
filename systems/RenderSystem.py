import pygame
import esper

from components import Renderable


class RenderSystem(esper.Processor):
    def __init__(self, screen, clear_color=(0, 0, 0)):
        super().__init__()
        self.screen = screen
        self.clear_color = clear_color

    def process(self):
        self.screen.fill(self.clear_color)
        for entity, renderable in self.world.get_component(Renderable):
            self.screen.blit(renderable.image, (renderable.x, renderable.y))
        pygame.display.flip()
