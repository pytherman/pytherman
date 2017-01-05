"""Pytherman main file"""

import Box2D
import esper
import pygame
from Box2D.b2 import edgeShape

import core
from components import Physics, Renderable, Velocity
from systems import MovementSystem, RenderSystem

FPS = 60
PPM = 20  # Pixels per meter (box2d scaling factor)
RESOLUTION = 720, 480
TIME_STEP = 1.0 / FPS


def setup_world_boundaries(pworld):
    """Sets static walls around board."""
    pworld.CreateStaticBody(
        position=(0, 0),
        shapes=edgeShape(vertices=((0, 0), (36, 0)))
    )
    pworld.CreateStaticBody(
        position=(0, 0),
        shapes=edgeShape(vertices=((0, 0), (0, 24)))
    )
    pworld.CreateStaticBody(
        position=(0, 0),
        shapes=edgeShape(vertices=((36, 24), (0, 24)))
    )
    pworld.CreateStaticBody(
        position=(0, 0),
        shapes=edgeShape(vertices=((36, 24), (36, 0)))
    )


def main():
    """Entry point for the game."""
    pygame.display.set_caption('Pytherman')
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 1)
    screen = pygame.display.set_mode(RESOLUTION)

    pworld = Box2D.b2.world(gravity=(0, 0), doSleep=True)
    setup_world_boundaries(pworld)

    world = esper.World()
    # Not sure if this is a good practice
    world.RESOLUTION = RESOLUTION
    world.PPM = PPM
    player = world.create_entity()
    player_image = pygame.image.load("assets/player.png")
    player_renderable = Renderable(image=player_image)
    player_body = pworld.CreateDynamicBody(position=(10, 10))
    player_body.CreatePolygonFixture(box=(player_renderable.w / world.PPM / 2,
                                          player_renderable.h / world.PPM / 2),
                                     density=1,
                                     friction=0.3)
    world.add_component(player, Physics(body=player_body))
    world.add_component(player, Velocity(x=0, y=0))
    world.add_component(player, player_renderable)

    enemy = world.create_entity()
    enemy_image = pygame.image.load("assets/enemy.png")
    enemy_renderable = Renderable(image=enemy_image)
    enemy_body = pworld.CreateDynamicBody(position=(20, 20))
    enemy_body.CreatePolygonFixture(box=(enemy_renderable.w / world.PPM / 2,
                                         enemy_renderable.h / world.PPM / 2),
                                    density=1,
                                    friction=0.3)
    world.add_component(enemy, Physics(body=enemy_body))
    world.add_component(enemy, enemy_renderable)

    render_system = RenderSystem(screen=screen)
    movement_system = MovementSystem()
    world.add_processor(render_system)
    world.add_processor(movement_system)

    event_handler = core.EventHandler(world=world, player=player)
    while event_handler.is_running():
        for event in pygame.event.get():
            event_handler.handle(event)
        pworld.Step(TIME_STEP, 10, 10)
        pworld.ClearForces()
        world.process()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
    pygame.quit()
