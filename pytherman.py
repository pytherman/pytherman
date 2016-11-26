import pygame
import esper

import core

from components import Velocity, Renderable
from systems import MovementSystem, RenderSystem


FPS = 60
RESOLUTION = 720, 480


def main():
    pygame.init()
    pygame.display.set_caption('Pytherman')
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 1)
    screen = pygame.display.set_mode(RESOLUTION)
    world = esper.World()
    player = world.create_entity()
    world.add_component(player, Velocity(x=0, y=0))
    player_image = pygame.image.load("assets/player.png")
    world.add_component(player, Renderable(image=player_image,
                                           x=100,
                                           y=100))
    enemy = world.create_entity()
    enemy_image = pygame.image.load("assets/enemy.png")
    world.add_component(enemy, Renderable(image=enemy_image,
                                          x=400,
                                          y=250))

    render_system = RenderSystem(screen=screen)
    movement_system = MovementSystem(minx=0,
                                     maxx=RESOLUTION[0],
                                     miny=0,
                                     maxy=RESOLUTION[1])
    world.add_processor(render_system)
    world.add_processor(movement_system)

    event_handler = core.EventHandler(world=world, player=player)
    while event_handler.is_running():
        for event in pygame.event.get():
            event_handler.handle(event)
        world.process()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
    pygame.quit()
