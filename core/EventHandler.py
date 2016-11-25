import pygame


class EventHandler(object):
    def __init__(self):
        self.running = True

    def handle(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False

    def is_running(self):
        return self.running