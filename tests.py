"""Unit tests for prepare_gamearea.py"""
import prepare_gamearea
import unittest


class PrepareGameareaTests(unittest.TestCase):
    """All test methods """

    def test_bfs_should_return_none(self):
        """test should return none for empty graph"""
        game_area = prepare_gamearea.PrepareGamearea(0, 0)
        score = prepare_gamearea.bfs(game_area.graph, (0, 0), (5, 0))
        self.assertEqual(score, None)

    def test_bfs_should_return_1_elem(self):
        """bfs should return list of one element when start and end point are the same"""
        game_area = prepare_gamearea.PrepareGamearea(1, 1)
        score = prepare_gamearea.bfs(game_area.graph, (0, 0), (0, 0))
        self.assertEqual(len(score), 1)

    def test_bfs_should_return_the_way(self):
        """test bfs should return the shortest way for full graph"""
        game_area = prepare_gamearea.PrepareGamearea(5, 5)
        score = prepare_gamearea.bfs(game_area.graph, (1, 1), (2, 2))
        self.assertEqual(len(score), 3)

    def test_bfs_should_return_none(self):
        """bfs should return none when we try to connect with border field"""
        game_area = prepare_gamearea.PrepareGamearea(5, 5)
        score = prepare_gamearea.bfs(game_area.graph, (1, 1), (4, 4))
        self.assertEqual(score, None)

    def test_bfs_should_return_none2(self):
        """bfs should return none when we path not exists"""
        game_area = {}
        score = prepare_gamearea.bfs(game_area, (1, 1), (4, 4))
        self.assertEqual(score, None)

    def test_if_path_exists_for_empty(self):
        """check if path exists should return false when graph is empty"""
        game_area = {}
        score = prepare_gamearea.check_if_path_exists(game_area, (0, 0), (1, 1))
        self.assertFalse(score)

    def test_check_if_path_exists_should_return_false_when_try_to_connect_with_border_field(self):
        game_area = prepare_gamearea.PrepareGamearea(5, 5)
        score = prepare_gamearea.bfs(game_area.graph, (1, 1), (4, 4))
        self.assertFalse(score)

    def test_check_if_path_exists_should_return_true_when_path_exists(self):
        game_area = prepare_gamearea.PrepareGamearea(5, 5)
        score = prepare_gamearea.bfs(game_area.graph, (1, 1), (3, 3))
        self.assertTrue(score)

    def prepare_gamearea_should_set_correct_number_of_rows(self):
        game_area = prepare_gamearea.PrepareGamearea(5, 5)
        self.assertEqual(game_area.number_of_rows, 5)

    def test_prepare_gamearea_should_set_correct_number_of_columns(self):
        game_area = prepare_gamearea.PrepareGamearea(5, 5)
        self.assertEqual(game_area.number_of_columns, 5)

    def test_init_of_prepare_gamearea_should_create_table_of_correct_number_of_rows(self):
        game_area = prepare_gamearea.PrepareGamearea(3, 3)
        self.assertEqual(len(game_area.table), 3)

    def test_init_of_prepare_gamearea_should_create_table_of_correct_number_of_columns(self):
        game_area = prepare_gamearea.PrepareGamearea(4, 4)
        self.assertEqual(len(game_area.table), 4)

    def test_init_of_prepare_gamearea_should_create_empty_graph_for_zeros_parameteres(self):
        game_area = prepare_gamearea.PrepareGamearea(0, 0)
        self.assertEqual(len(game_area.graph), 0)

    def test_prepare_gamearea_should_ignore_border_nodes(self):
        game_area = prepare_gamearea.PrepareGamearea(3, 3)
        tmp = {(1, 1): []}
        self.assertEqual(game_area.graph, tmp)

    def test_prepare_gamearea_should_create_correct_graph_for_small_board(self):
        game_area = prepare_gamearea.PrepareGamearea(4, 4)
        tmp = {(1, 1): [(2, 1), (1, 2)],
               (1, 2): [(2, 2), (1, 1)],
               (2, 1): [(1, 1), (2, 2)],
               (2, 2): [(1, 2), (2, 1)]}
        self.assertEqual(game_area.graph, tmp)

    def test_prepare_list_of_special_fields_should_be_empty_for_empty_board(self):
        game_area = prepare_gamearea.PrepareGamearea(0, 0)
        list = game_area.prepare_list_of_special_fields()
        self.assertEqual(list, [])

    def test_prepare_list_of_special_fields_should_not_containa_fields_closest_to_player(self):
        game_area = prepare_gamearea.PrepareGamearea(5, 5)
        list = game_area.prepare_list_of_special_fields()
        flag = False
        if (1, 1) in list:
            flag = True
        if (2, 1) in list:
            flag = True
        if (1, 2) in list:
            flag = True
        self.assertFalse(flag)

    def test_prepare_list_of_special_fields_should_not_containa_fields_closest_to_enemy(self):
        game_area = prepare_gamearea.PrepareGamearea(5, 5)
        list = game_area.prepare_list_of_special_fields()
        flag = False
        if (game_area.number_of_rows - 2, game_area.number_of_columns - 2) in list:
            flag = True
        if (game_area.number_of_rows - 3, game_area.number_of_columns - 2) in list:
            flag = True
        if (game_area.number_of_rows - 2, game_area.number_of_columns - 3) in list:
            flag = True
        self.assertFalse(flag)

    def test_prepare_should_return_correct_list_for_small_area(self):
        game_area = prepare_gamearea.PrepareGamearea(5, 5)
        list = sorted(game_area.prepare_list_of_special_fields())
        tmp = [(1, 3), (2, 2), (3, 1)]
        self.assertEqual(tmp, list)

    def test_prepare_should_return_correct_list_for_bigger_area(self):
        game_area = prepare_gamearea.PrepareGamearea(7, 7)
        list = sorted(game_area.prepare_list_of_special_fields())
        tmp = [(1, 3), (1, 4), (1, 5),
               (2, 2), (2, 3), (2, 4), (2, 5),
               (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
               (4, 1), (4, 2), (4, 3), (4, 4),
               (5, 1), (5, 2), (5, 3)]
        self.assertEqual(tmp, list)

    def test_before_set_door_field_position_of_door_should_be_minus_one(self):
        game_area = prepare_gamearea.PrepareGamearea(5, 5)
        self.assertEqual((-1, -1), (game_area.door_field_x, game_area.door_field_y))

    def test_after_set_door_field_position_of_door_should_not_be_minus_one(self):
        game_area = prepare_gamearea.PrepareGamearea(5, 5)
        game_area.set_door_field(game_area.prepare_list_of_special_fields())
        self.assertNotEqual((-1, -1), (game_area.door_field_x,
                                       game_area.door_field_y))

    def test_after_set_door_field_on_certain_position_in_table_should_be_value_three(self):
        game_area = prepare_gamearea.PrepareGamearea(5, 5)
        game_area.set_door_field(game_area.prepare_list_of_special_fields())
        self.assertEqual(game_area.table[game_area.door_field_x][game_area.door_field_y], 3)

    def test_create_table_of_game_should_not_be_empty(self):
        game_area = prepare_gamearea.PrepareGamearea(5, 5)
        arr = game_area.create_table_of_game()
        self.assertTrue(isinstance(arr, list))

    def test_create_table_should_have_value_of_three_where_door_is_placed(self):
        game_area = prepare_gamearea.PrepareGamearea(9, 9)
        arr = game_area.create_table_of_game()
        x = game_area.door_field_x
        y = game_area.door_field_y
        self.assertEqual(arr[x][y], 3)

    def test_set_fields_should_return_list(self):
        game_area = prepare_gamearea.PrepareGamearea(5, 5)
        arr = game_area.set_fields(3, [(1, 1), (1, 2), (2, 2)], 2)
        self.assertTrue(isinstance(arr, list))

    def test_set_fields_should_return_shorter_list_when_fields_were_added(self):
        game_area = prepare_gamearea.PrepareGamearea(5, 5)
        arr = game_area.set_fields(3, [(1, 1), (1, 2), (2, 2)], 2)
        self.assertLess(len(arr), 3)

    def test_set_fields_should_return_the_same_list_when_fields_were_not_added(self):
        game_area = prepare_gamearea.PrepareGamearea(5, 5)
        arr = game_area.set_fields(0, [(1, 1), (1, 2), (2, 2)], 2)
        self.assertEqual(arr, [(1, 1), (1, 2), (2, 2)])

    def test_set_fields_without_checking_path_should_return_list(self):
        game_area = prepare_gamearea.PrepareGamearea(5, 5)
        arr = game_area.set_fields_without_checking_path(3, [(1, 1), (1, 2), (2, 2)], 2)
        self.assertTrue(isinstance(arr, list))

    def test_set_fields_without_checking_should_return_shorter_list_when_fields_were_added(self):
        game_area = prepare_gamearea.PrepareGamearea(5, 5)
        arr = game_area.set_fields_without_checking_path(3, [(1, 1), (1, 2), (2, 2)], 2)
        self.assertLess(len(arr), 3)

    def test_set_fields_without_check_should_return_the_same_list_when_fields_were_not_added(self):
        game_area = prepare_gamearea.PrepareGamearea(5, 5)
        arr = game_area.set_fields_without_checking_path(0, [(1, 1), (1, 2), (2, 2)], 2)
        self.assertEqual(arr, [(1, 1), (1, 2), (2, 2)])


suite = unittest.TestLoader().loadTestsFromTestCase(PrepareGameareaTests)
print(unittest.TextTestRunner(verbosity=3).run(suite))
