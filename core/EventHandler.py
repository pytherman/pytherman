import pygame


from components import Velocity


class EventHandler(object):
    def __init__(self, world, player):
        self.world = world
        self.player = player
        self.running = True

    def handle(self, event):
        if event.type == pygame.QUIT:
                self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.world.component_for_entity(self.player, Velocity).x = -3
            elif event.key == pygame.K_RIGHT:
                self.world.component_for_entity(self.player, Velocity).x = 3
            elif event.key == pygame.K_UP:
                self.world.component_for_entity(self.player, Velocity).y = -3
            elif event.key == pygame.K_DOWN:
                self.world.component_for_entity(self.player, Velocity).y = 3
            elif event.key == pygame.K_ESCAPE:
                self.running = False
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.world.component_for_entity(self.player, Velocity).x = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                self.world.component_for_entity(self.player, Velocity).y = 0

    def is_running(self):
        return self.running
