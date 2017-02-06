"""Event handler"""


import pygame

from messaging import Intent, IntentMessage


class EventHandler(object):
    """EventHandler is responsible for parsing user input - pygame events.
    It is the only place where input is being consumed by the game."""

    def __init__(self, world, screen):
        self.world = world
        self.running = True
        self.screen = screen

    def handle(self, event):
        """Handles pygame event."""

        player = self.world.player
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.world.msg_bus.add(IntentMessage(player, Intent.MOVE_LEFT))
            elif event.key == pygame.K_RIGHT:
                self.world.msg_bus.add(IntentMessage(player, Intent.MOVE_RIGHT))
            elif event.key == pygame.K_UP:
                self.world.msg_bus.add(IntentMessage(player, Intent.MOVE_UP))
            elif event.key == pygame.K_DOWN:
                self.world.msg_bus.add(IntentMessage(player, Intent.MOVE_DOWN))
            elif event.key == pygame.K_RETURN:
                self.world.msg_bus.add(IntentMessage(player, Intent.PLANT_BOMB))
            elif event.key == pygame.K_ESCAPE:
                self.running = False
                from mainmenu import Menu
                gm = Menu(self.screen)
                gm.run()
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.world.msg_bus.add(IntentMessage(player, Intent.MOVE_CLEAR_HORIZONTAL))
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                self.world.msg_bus.add(IntentMessage(player, Intent.MOVE_CLEAR_VERTICAL))

    def is_running(self):
        """Checks if the game is still running."""

        return self.running
