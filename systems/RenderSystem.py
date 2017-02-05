"""Render system"""

import esper
import pygame
import sys

from components import Physics, Renderable, Bomber, Bonus, Health
from statboard import Statboard


class RenderSystem(esper.Processor):
    """Responsible for rendering entities on screen."""

    def __init__(self, screen, player, world, clear_color=(0, 0, 0)):
        super().__init__()
        self.screen = screen
        self.clear_color = clear_color
        self.statboard = Statboard(screen)
        self.world = world
        self.player = player

    def process(self):
        self.screen.fill(self.clear_color)
        for _, (renderable,
                physics) in self.world.get_components(Renderable, Physics):
            body = physics.body
            # Currently this is used to draw a debug physics shapes
            for fixture in body.fixtures:
                shape = fixture.shape
                # We need to transform vertices from box2d prespective
                # to pygame prespective - first scaling
                vertices = [(body.transform * v) *
                            self.world.PPM for v in shape.vertices]
                # Then we need to transform coordinate system
                # box2d uses standard one, pygame uses one with (0,0)
                # in top left corner
                vertices = [(v[0],
                             self.world.RESOLUTION[1] - v[1])
                            for v in vertices]
                pygame.draw.polygon(self.screen,
                                    (0, 0, 255, 255),
                                    vertices)
            # We need to apply the very same transformation as for
            # debug drawing, but also we need to keep in mind that
            # the point in which image will be rendered will be
            # the top left corner of the image, not center
            v = [v * self.world.PPM for v in body.position]
            v = [v[0] - renderable.w / 2,
                 self.world.RESOLUTION[1] - v[1] - renderable.h / 2]
            self.screen.blit(renderable.image, v)
        try:
            hp = (self.world.component_for_entity(self.player, Health))
        except KeyError:
            print("Jesteś looserem!")
            sys.exit()
        self.statboard.hp = hp.hp
        bombs = self.world.component_for_entity(self.player, Bomber)
        self.statboard.bombs = bombs.max - bombs.used
        self.statboard.blit()
        pygame.display.flip()
