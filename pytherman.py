"""Pytherman main file"""

import Box2D
import esper
import pygame
from Box2D.b2 import edgeShape

import core
import drawboard
from components import Bomber, Physics, Renderable, Velocity
from messaging import MessageBus
from systems import (ActionSystem, BonusSystem, DamageSystem, ExplosionSystem,
                     MovementSystem, RenderSystem)

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
    world.pworld = pworld
    world.screen = screen
    world.to_delete = set()

    # Not sure if this is a good practice
    world.RESOLUTION = RESOLUTION
    world.PPM = PPM
    world.msg_bus = MessageBus()
    drawboard.draw_board(pworld, world, PPM, RESOLUTION)

    _setup_player(world)
    _setup_enemy(world)
    _setup_systems(world, screen)

    event_handler = core.EventHandler(world=world)
    while event_handler.is_running():
        for event in pygame.event.get():
            event_handler.handle(event)
        pworld.Step(TIME_STEP, 10, 10)
        pworld.ClearForces()
        world.process()
        clock.tick(FPS)
        world.msg_bus.clear()
        for entity in world.to_delete:
            _cleanup_entity(world, entity)
        world.to_delete = set()


def _cleanup_entity(world, entity):
    physics = world.component_for_entity(
        entity,
        Physics)
    if physics.body:
        world.pworld.DestroyBody(physics.body)
        physics.body = None
    world.delete_entity(entity)


def _setup_systems(world, screen):
    render_system = RenderSystem(screen=screen)
    world.add_processor(render_system)
    movement_system = MovementSystem()
    world.add_processor(movement_system)
    action_system = ActionSystem()
    world.add_processor(action_system)
    explosion_system = ExplosionSystem()
    world.add_processor(explosion_system)
    damage_system = DamageSystem()
    world.add_processor(damage_system)
    bonus_system = BonusSystem()
    world.add_processor(bonus_system)


def _setup_player(world):
    player = world.create_entity()
    shift = 3 * 40 / 2  # change 40 to field_size
    world.player = player
    player_image = pygame.image.load("assets/player.png")
    player_renderable = Renderable(image=player_image)
    player_body = world.pworld.CreateDynamicBody(
        position=(shift / PPM, shift / PPM))
    player_body.fixedRotation = True
    player_body.CreatePolygonFixture(
        box=(player_renderable.w / world.PPM / 2 - 0.2,
             player_renderable.h / world.PPM / 2 - 0.2),
        density=1,
        friction=0.3)
    world.add_component(player, Physics(body=player_body))
    world.add_component(player, Velocity(x=0, y=0))
    world.add_component(player, player_renderable)
    world.add_component(player, Bomber(max=3, cooldown=2))


def _setup_enemy(world):
    enemy = world.create_entity()
    enemy_image = pygame.image.load("assets/enemy.png")
    enemy_renderable = Renderable(image=enemy_image)
    shift = 3 * 40 / 2  #change 40 to field_size
    enemy_body = world.pworld.CreateDynamicBody(
        position=((RESOLUTION[0] - shift) / PPM,
                  (RESOLUTION[1] - shift) / PPM))
    enemy_body.CreatePolygonFixture(
        box=(enemy_renderable.w / world.PPM / 2 - 0.2,
             enemy_renderable.h / world.PPM / 2 - 0.2),
        density=1,
        friction=0.3)
    world.add_component(enemy, Physics(body=enemy_body))
    world.add_component(enemy, enemy_renderable)


if __name__ == '__main__':
    main()
    pygame.quit()
