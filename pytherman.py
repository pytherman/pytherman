import pygame
import esper

import Box2D
from Box2D.b2 import (polygonShape, staticBody, dynamicBody)

import core

from components import (Velocity, Renderable, Position)
from systems import MovementSystem, RenderSystem


FPS = 60
RESOLUTION = 720, 480

class Pytherman:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Pytherman')
        clock = pygame.time.Clock()
        pygame.key.set_repeat(1, 1)
        screen = pygame.display.set_mode(RESOLUTION)
        world = esper.World()

        pworld = Box2D.b2.world(gravity=(0, -10), doSleep=True)

        ground_body = pworld.CreateStaticBody(
            position=(0, 1),
            shapes=polygonShape(box=(50, 5)),
        )

        player = world.create_entity()
        world.add_component(player, Velocity(x=0, y=0))
        world.add_component(player, Position(x=100, y=100))
        player_image = pygame.image.load("assets/player.png")
        world.add_component(player, Renderable(image=player_image))
        enemy = world.create_entity()
        world.add_component(enemy, Position(x=400, y=250))
        enemy_image = pygame.image.load("assets/enemy.png")
        world.add_component(enemy, Renderable(image=enemy_image))

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
    Pytherman.pytherman()
    pygame.quit()
