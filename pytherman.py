import pygame

import core

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Pytherman')
    background = pygame.Surface(screen.get_size())
    background.fill((255, 255, 255))
    background = background.convert()
    event_handler = core.EventHandler()

    while event_handler.is_running():
        for event in pygame.event.get():
            event_handler.handle(event)
        screen.blit(background, (0, 0))
        pygame.display.update()

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
