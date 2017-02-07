"""Pytherman main file"""

import Box2D
import esper
import pygame
from Box2D.b2 import edgeShape
from Box2D import b2ContactListener

import core
import drawboard
from components import Bomber, Physics, Renderable, Velocity, Health, Bonus, Explodable, AIControllable
from messaging import MessageBus
from systems import (ActionSystem, BonusSystem, DamageSystem, ExplosionSystem,
                     MovementSystem, RenderSystem, AISystem)

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

    world = esper.World()

    pworld = Box2D.b2.world(
        gravity=(0, 0),
        doSleep=True,
        contactListener=PythermanContactListener(world=world))
    setup_world_boundaries(pworld)

    world.pworld = pworld
    world.screen = screen
    world.to_delete = set()
    world.level = 1
    world.next_level = False

    # Not sure if this is a good practice
    world.RESOLUTION = RESOLUTION
    world.PPM = PPM
    world.msg_bus = MessageBus()
    drawboard.draw_board(pworld, world, PPM,
                         (RESOLUTION[0], RESOLUTION[1] - 40))  # TODO - change that to something prettier

    player = _setup_player(world)
    _setup_enemy(world)
    _setup_systems(world, screen, player)

    event_handler = core.EventHandler(world=world, screen=screen)
    while event_handler.is_running():
        if world.next_level:
            tmp = world
            world = esper.World()
            pworld = Box2D.b2.world(
                gravity=(0, 0),
                doSleep=True,
                contactListener=PythermanContactListener(world=world))
            setup_world_boundaries(pworld)

            world.pworld = pworld
            world.screen = screen
            world.to_delete = set()
            print("next level!")
            world.next_level = False
            world.level = tmp.level + 1
            x, y = tmp.RESOLUTION
            y += 40
            world.RESOLUTION = (x, y)
            world.PPM = PPM
            screen = pygame.display.set_mode(world.RESOLUTION)
            world.msg_bus = MessageBus()
            drawboard.draw_board(pworld, world, PPM,
                                 (world.RESOLUTION[0], world.RESOLUTION[1] - 40))
            _setup_enemy(world)
            player = _setup_player(world)
            _setup_systems(world, screen, player)
            event_handler = core.EventHandler(world=world, screen=screen)
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
    """Delete entity from world with all its components"""
    physics = world.component_for_entity(
        entity,
        Physics)
    if physics.body:
        world.pworld.DestroyBody(physics.body)
        physics.body = None
    world.delete_entity(entity)


def _setup_systems(world, screen, player):
    """Setup all systems in world"""
    render_system = RenderSystem(screen=screen, world=world, player=player)
    world.add_processor(render_system)
    ai_system = AISystem()
    world.add_processor(ai_system)
    movement_system = MovementSystem()
    world.add_processor(movement_system)
    action_system = ActionSystem()
    world.add_processor(action_system)
    explosion_system = ExplosionSystem(screen=screen, resolution=RESOLUTION)
    world.add_processor(explosion_system)
    damage_system = DamageSystem()
    world.add_processor(damage_system)
    bonus_system = BonusSystem()
    world.add_processor(bonus_system)


def _setup_player(world):
    """Create new player with all its components and add it to world"""
    player = world.create_entity()
    shift = 3 * 40 / 2  # change 40 to field_size
    world.player = player
    player_image = pygame.image.load("assets/player.png")
    player_renderable = Renderable(image=player_image)
    player_body = world.pworld.CreateDynamicBody(
        position=(shift / PPM, shift / PPM))
    player_body.userData = player
    player_body.fixedRotation = True
    player_body.CreatePolygonFixture(
        box=(player_renderable.w / world.PPM / 2 - 0.2,
             player_renderable.h / world.PPM / 2 - 0.2),
        density=1,
        friction=0.3)
    world.add_component(player, Physics(body=player_body))
    world.add_component(player, Velocity(x=0, y=0))
    world.add_component(player, player_renderable)
    world.add_component(player, Bomber(max=3, cooldown=0.5))
    world.add_component(player, Health(hp=5))
    return player


def _setup_enemy(world):
    """Create new enemy with all its components and add it to world"""
    enemy = world.create_entity()
    print("enemy id {}".format(enemy))
    enemy_image = pygame.image.load("assets/enemy.png")
    enemy_renderable = Renderable(image=enemy_image)
    shift = 3 * 40 / 2  # change 40 to field_size
    enemy_body = world.pworld.CreateDynamicBody(
        position=((world.RESOLUTION[0] - shift) / world.PPM,
                  (world.RESOLUTION[1] - 40 - shift) / world.PPM))
    enemy_body.userData = enemy
    enemy_body.fixedRotation = True
    enemy_body.CreatePolygonFixture(
        box=(enemy_renderable.w / world.PPM / 2 - 0.2,
             enemy_renderable.h / world.PPM / 2 - 0.2),
        density=1,
        friction=0.3)
    enemy_body.userData = enemy
    world.add_component(enemy, Physics(body=enemy_body))
    world.add_component(enemy, enemy_renderable)
    world.add_component(enemy, AIControllable())
    world.add_component(enemy, Bomber(max=3, cooldown=4))
    world.add_component(enemy, Velocity(x=0, y=0))


class PythermanContactListener(b2ContactListener):
    def __init__(self, world):
        b2ContactListener.__init__(self)
        self.world = world

    def BeginContact(self, contact):
        pass

    def EndContact(self, contact):
        entity_a = contact.fixtureA.body.userData
        entity_b = contact.fixtureB.body.userData
        player = -1
        bomb = -1
        if entity_a == self.world.player:
            player = entity_a
            bomb = entity_b
        if entity_b == self.world.player:
            player = entity_b
            bomb = entity_a
        if player != -1 and bomb != -1:
            try:
                b = self.world.component_for_entity(bomb, Explodable)
                b.clean = True
            except KeyError:
                pass

    def PreSolve(self, contact, oldManifold):
        entity_a = contact.fixtureA.body.userData
        entity_b = contact.fixtureB.body.userData
        player = -1
        bonus = -1
        if entity_a == self.world.player:
            player = entity_a
            bonus = entity_b
        if entity_b == self.world.player:
            player = entity_b
            bonus = entity_a
        if player != -1 and bonus != -1:
            try:
                b = self.world.component_for_entity(bonus, Bonus)
                b.on_pickup(self.world, player)
                self.world.to_delete.add(bonus)
                contact.enabled = False
            except KeyError:
                try:
                    b = self.world.component_for_entity(bonus, Explodable)
                    if not b.clean:
                        contact.enabled = False
                except KeyError:
                    pass

    def PostSolve(self, contact, impulse):
        pass


if __name__ == '__main__':
    main()
    pygame.quit()
