"""
Prepare dimensional table of area of game where:
0 means empty field
1 means field with wooden wall
2 means field with concrete wall
3 means field with door to the next level

Class check also if the paths to the enemy and the door exist
"""

import copy
import random


def bfs(graph_to_search, start, end):
    """Find the shortest way from start to end using
    breadth-first search algorithm. Function returns list of nodes
    in the shortest way"""
    queue = [[start]]
    visited = set()

    while queue:
        path = queue.pop(0)
        vertex = path[-1]
        if vertex == end:
            return path
        elif vertex not in visited:
            for current_neighbour in graph_to_search.get(vertex, []):
                new_path = list(path)
                new_path.append(current_neighbour)
                queue.append(new_path)
                if current_neighbour == end:
                    return new_path
            visited.add(vertex)


def check_if_path_exists(graph, start, end):
    """Return true if path from start to end exists,
    otherwise returns false"""
    return bfs(graph, start, end) is not None


class PrepareGamearea:
    """Return a board of game with places for special fields"""

    def __init__(self, number_of_rows, number_of_columns):
        """Set up all variables in class"""
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.table = [[0 for _ in range(self.number_of_columns)] for _ in range(self.number_of_rows)]
        self.graph = self.generate_graph()
        self.door_field_x = -1
        self.door_field_y = -1

    def generate_graph(self):
        """Function returns graph with all existing
        paths between nodes. Function ignores connections with bordered walls"""
        self.graph = {}
        for i in range(1, self.number_of_columns - 1):
            for j in range(1, self.number_of_rows - 1):
                nodes = []
                if i > 1:
                    nodes.append((i - 1, j))
                if i < self.number_of_columns - 2:
                    nodes.append((i + 1, j))
                if j > 1:
                    nodes.append((i, j - 1))
                if j < self.number_of_rows - 2:
                    nodes.append((i, j + 1))
                self.graph[(i, j)] = nodes
        return self.graph

    def prepare_list_of_special_fields(self):
        """Return basic list of tiles where special walls can be placed.
        From list were removed the closest to main character and enemy fields.
        From list are also removed border tiles where solid borders are placed."""
        fields_to_add = []
        for i in range(1, self.number_of_rows - 1):
            for j in range(1, self.number_of_columns - 1):
                fields_to_add.append((i, j))

        if (1, 1) in fields_to_add:
            fields_to_add.remove((1, 1))
        if (2, 1) in fields_to_add:
            fields_to_add.remove((2, 1))
        if (1, 2) in fields_to_add:
            fields_to_add.remove((1, 2))
        if (self.number_of_rows - 2, self.number_of_columns - 2) in fields_to_add:
            fields_to_add.remove((self.number_of_rows - 2, self.number_of_columns - 2))
        if (self.number_of_rows - 3, self.number_of_columns - 2) in fields_to_add:
            fields_to_add.remove((self.number_of_rows - 3, self.number_of_columns - 2))
        if (self.number_of_rows - 2, self.number_of_columns - 3) in fields_to_add:
            fields_to_add.remove((self.number_of_rows - 2, self.number_of_columns - 3))
        return fields_to_add

    def set_fields(self, number, list_to_add, value):
        """Function marks fields where number of solid walls should be placed.
        Fields are finding randomly. Before marking field bfs algorithm checks
        if after adding path from start to hidden door and enemy will exists.
        Function return list where the rest of special fields can be placed"""
        for i in range(number):
            x, y = (random.choice(list_to_add))
            tmp = copy.deepcopy(self.graph)
            tmp[(y, x)] = []
            for j in tmp:
                if (y, x) in tmp[j]:
                    tmp[j].remove((y, x))
            if check_if_path_exists(tmp, (1, 1), (self.number_of_columns - 2, self.number_of_rows - 2)):
                self.table[x][y] = value
                self.graph = copy.deepcopy(tmp)
            list_to_add.remove((x, y))
        return list_to_add

    def set_fields_without_checking_path(self, number, list_to_add, value):
        """Function finds the number of fields where special field
        (given by value parameter) should be placed. Fields are chosen randomly.
        Special fields must be destroyable, so we don't have to check if after adding special filed
        path exists. Function returns list of tiles where special fields can be added."""
        for i in range(number):
            x, y = (random.choice(list_to_add))
            self.table[x][y] = value
            list_to_add.remove((x, y))
        return list_to_add

    def set_door_field(self, list_to_add):
        """Function randomly find a place where door hidden
        by wooden wall should be placed. Function return list
        of tiles where the rest of special fields should be placed."""
        while self.door_field_x == -1:
            x, y = (random.choice(list_to_add))
            self.table[x][y] = 3
            self.door_field_x = x
            self.door_field_y = y
            list_to_add.remove((x, y))
        return list_to_add

    def create_table_of_game(self):
        """Function control creating area of game - use
        helper functions to mark places for walls and hidden door.
        Function return table where each tiles is mark by number
        meaning which kind of wall should be placed on it."""
        list_to_add = self.prepare_list_of_special_fields()
        number_of_special_fields = int(0.9 * (len(list_to_add) - 1))
        number_of_wooden_fields = int(0.6 * number_of_special_fields)
        number_of_concrete_fields = int(0.4 * number_of_special_fields)

        list_to_add = self.set_door_field(list_to_add)
        list_to_add = self.set_fields(number_of_concrete_fields, list_to_add, 2)
        list_to_add = self.set_fields_without_checking_path(number_of_wooden_fields, list_to_add, 1)
        return self.table
