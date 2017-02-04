"""draw area of game"""

import pygame

from components import Health, Physics, Renderable, Treasure
from prepare_gamearea import PrepareGamearea


def draw_board(pworld, world, PPM, RESOLUTION):
    """Draw all fields on gamearea"""
    width, height = RESOLUTION
    wooden_field_image = pygame.image.load("assets/fields/woden_big_lines.png")
    wooden_field_renderable = Renderable(image=wooden_field_image)
    field_size = wooden_field_renderable.w
    number_of_columns = int(width / field_size)
    number_of_rows = int(height / field_size)
    game_area = PrepareGamearea(number_of_rows, number_of_columns).create_table_of_game()

    for i in range(1, number_of_rows - 1):
        for j in range(1, number_of_columns - 1):
            draw_field(world, pworld, PPM, i, j, 0)
            draw_field(world, pworld, PPM, i, j, game_area[i][j])

    draw_border_walls(pworld, world, PPM, RESOLUTION)


def draw_field(world, pworld, PPM, y, x, value):
    """Draw the special type of field decided by given parameter value"""
    if value == 0:
        draw_grass_field(world, pworld, PPM, x, y)
    elif value == 1:
        draw_wooden_field(world, pworld, PPM, x, y)
    elif value == 2:
        draw_concrete_field(world, pworld, PPM, x, y)
    else:
        draw_door_field(world, pworld, PPM, x, y)


def draw_grass_field(world, pworld, PPM, x, y):
    """draw grass field on given position"""
    field_image = pygame.image.load("assets/fields/grass_lines.png")
    field_renderable = Renderable(image=field_image)
    field_size = field_renderable.w
    field_size = int(field_size / PPM)
    create_field(world, pworld, field_size / 2 + x * field_size,
                 field_size / 2 + y * field_size, field_renderable)


def draw_wooden_field(world, pworld, PPM, x, y):
    """draw wooden wall on given position"""
    field_image = pygame.image.load("assets/fields/woden_big_lines.png")
    field_renderable = Renderable(image=field_image)
    field_size = field_renderable.w
    field_size = int(field_size / PPM)
    create_field_with_physics(world, pworld, x * field_size + field_size / 2, y * field_size + field_size / 2,
                              field_size, field_renderable)


def draw_concrete_field(world, pworld, PPM, x, y):
    """draw concrete wall on given position"""
    field_image = pygame.image.load("assets/fields/concrete_drops.png")
    field_renderable = Renderable(image=field_image)
    field_size = field_renderable.w
    field_size = int(field_size / PPM)
    create_static_field(world, pworld, x * field_size + field_size / 2, y * field_size + field_size / 2,
                        field_size, field_renderable)


def draw_door_field(world, pworld, PPM, x, y):
    """draw wooden wall with hidden door on given position"""
    field_image = pygame.image.load("assets/fields/hard_wall.png")
    field_renderable = Renderable(image=field_image)
    field_size = field_renderable.w
    field_size = int(field_size / PPM)
    create_field_with_physics(world, pworld, x * field_size + field_size / 2, y * field_size + field_size / 2,
                              field_size, field_renderable)


def create_field(world, pworld, position_x, position_y, field_renderable):
    """create field without physics with image from paramteres on given position"""
    field = world.create_entity()
    field_body = pworld.CreateStaticBody(
        position=(position_x, position_y))
    world.add_component(field, Physics(body=field_body))
    world.add_component(field, field_renderable)


def create_static_field(world, pworld, position_x, position_y, field_size, field_renderable):
    """draw static field with image from parameters on given position"""
    field = world.create_entity()
    field_body = pworld.CreateStaticBody(
        position=(position_x, position_y),
        userData=field)
    field_body.CreatePolygonFixture(box=(field_size / 2,
                                         field_size / 2),
                                    density=234,
                                    friction=0.3)
    world.add_component(field, Physics(body=field_body))
    world.add_component(field, field_renderable)


def create_field_with_physics(world, pworld, position_x, position_y, field_size, field_renderable):
    """Draw field with physics with image from parameters on given position"""
    field = world.create_entity()
    field_body = pworld.CreateDynamicBody(
        position=(position_x, position_y),
        userData=field)
    field_body.fixedRotation = True
    field_body.CreatePolygonFixture(box=(field_size / 2 - 0.1,
                                         field_size / 2 - 0.1),
                                    density=1000000,
                                    friction=0.3)
    world.add_component(field, Physics(body=field_body))
    world.add_component(field, field_renderable)
    world.add_component(field, Health(hp=2))
    world.add_component(field, Treasure(chance=0.5))


def draw_border_walls(pworld, world, PPM, RESOLUTION):
    """Draw border walls around the gamearea"""
    field_image = pygame.image.load("assets/fields/hard_wall.png")
    field_renderable = Renderable(image=field_image)

    width, height = RESOLUTION
    field_size = field_renderable.w
    number_of_columns = int(width / field_size)
    number_of_rows = int(height / field_size)
    field_size = int(field_size / PPM)

    for i in range(number_of_columns):
        create_static_field(world, pworld, field_size / 2 + i * field_size, field_size / 2,
                            field_size, field_renderable)
        create_static_field(world, pworld, field_size / 2 + i * field_size,
                            number_of_rows * field_size - field_size / 2, field_size,
                            field_renderable)

    for i in range(1, number_of_rows - 1):
        create_static_field(world, pworld, field_size / 2, field_size / 2 + i * field_size,
                            field_size, field_renderable)
        create_static_field(world, pworld, number_of_columns * field_size - field_size / 2,
                            field_size / 2 + i * field_size, field_size, field_renderable)
