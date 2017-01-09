"""draw area of game"""

import random

import pygame

from components import Physics, Renderable


def create_field(world, pworld, position_x, position_y, field_renderable):
    """create field without physics"""
    field = world.create_entity()
    field_body = pworld.CreateStaticBody(
        position=(position_x, position_y))
    world.add_component(field, Physics(body=field_body))
    world.add_component(field, field_renderable)


def create_field_with_physics(world, pworld, position_x, position_y, field_size, field_renderable):
    """draw field with physics"""
    field = world.create_entity()
    field_body = pworld.CreateStaticBody(
        position=(position_x, position_y))
    field_body.CreatePolygonFixture(box=(field_size / 2,
                                         field_size / 2),
                                    density=1,
                                    friction=0.3)
    world.add_component(field, Physics(body=field_body))
    world.add_component(field, field_renderable)


def prepare_list_of_fields_to_add_special_walls(resolution, field_size):
    width, height = resolution
    number_of_columns = int(width / field_size) - 1
    number_of_rows = int(height / field_size) - 1

    fields_to_add = []
    for i in range(1, number_of_columns):
        for j in range(1, number_of_rows):
            fields_to_add.append((i, j))

    fields_to_add.remove((1, 1))
    fields_to_add.remove((2, 1))
    fields_to_add.remove((1, 2))
    fields_to_add.remove((number_of_columns - 2, number_of_rows - 1))
    fields_to_add.remove((number_of_columns - 1, number_of_rows - 1))
    fields_to_add.remove((number_of_columns - 1, number_of_rows - 2))
    return fields_to_add


def draw_special_fields(world, pworld, PPM, RESOLUTION):
    """draw fields with concrete and wooden walls """
    wooden_field_image = pygame.image.load("assets/fields/woden_big_lines.png")
    wooden_field_renderable = Renderable(image=wooden_field_image)
    concrete_field_image = pygame.image.load("assets/fields/concrete_drops.png")
    concrete_field_renderable = Renderable(image=concrete_field_image)
    field_size = concrete_field_renderable.w / PPM

    fields_to_add_walls = prepare_list_of_fields_to_add_special_walls(RESOLUTION, concrete_field_renderable.w)
    number_of_special_fields = int(0.8 * len(fields_to_add_walls))
    number_of_wooden_fields = int(0.4 * number_of_special_fields)
    number_of_concrete_fields = int(0.6 * number_of_special_fields)

    for i in range(number_of_wooden_fields):
        x, y = (random.choice(fields_to_add_walls))
        create_field_with_physics(world, pworld, x * field_size + field_size / 2, y * field_size + field_size / 2,
                                  field_size, wooden_field_renderable)
        fields_to_add_walls.remove((x, y))

    for i in range(number_of_concrete_fields):
        x, y = (random.choice(fields_to_add_walls))
        create_field_with_physics(world, pworld, x * field_size + field_size / 2, y * field_size + field_size / 2,
                                  field_size, concrete_field_renderable)
        fields_to_add_walls.remove((x, y))


def draw_board(pworld, world, PPM, RESOLUTION):
    """prepare board """
    draw_border_walls(pworld, world, PPM, RESOLUTION)
    draw_grass(world, pworld, PPM, RESOLUTION)
    draw_special_fields(world, pworld, PPM, RESOLUTION)


def draw_grass(world, pworld, PPM, RESOLUTION):
    """draw all green fields"""
    field_image = pygame.image.load("assets/fields/grass_lines.png")
    field_renderable = Renderable(image=field_image)

    width, height = RESOLUTION
    field_size = field_renderable.w
    number_of_columns = int(width / field_size)
    number_of_rows = int(height / field_size)
    field_size = int(field_size / PPM)

    for i in range(1, number_of_columns - 1):
        for j in range(1, number_of_rows - 1):
            create_field(world, pworld, field_size / 2 + i * field_size,
                         field_size / 2 + j * field_size, field_renderable)


def draw_border_walls(pworld, world, PPM, RESOLUTION):
    """draw border walls"""
    field_image = pygame.image.load("assets/fields/hard_wall.png")
    field_renderable = Renderable(image=field_image)

    width, height = RESOLUTION
    field_size = field_renderable.w
    number_of_columns = int(width / field_size)
    number_of_rows = int(height / field_size)
    field_size = int(field_size / PPM)

    for i in range(number_of_columns):
        create_field_with_physics(world, pworld, field_size / 2 + i * field_size, field_size / 2,
                                  field_size, field_renderable)
        create_field_with_physics(world, pworld, field_size / 2 + i * field_size,
                                  number_of_rows * field_size - field_size / 2, field_size,
                                  field_renderable)

    for i in range(1, number_of_rows - 1):
        create_field_with_physics(world, pworld, field_size / 2, field_size / 2 + i * field_size,
                                  field_size, field_renderable)
        create_field_with_physics(world, pworld, number_of_columns * field_size - field_size / 2,
                                  field_size / 2 + i * field_size, field_size, field_renderable)
