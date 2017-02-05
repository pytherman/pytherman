import prepare_gamearea
import unittest


class prepare_gamearea_tests(unittest.TestCase):
    def test_bfs_should_return_none_for_empty_graph(self):
        ga = prepare_gamearea.PrepareGamearea(0, 0)
        score = prepare_gamearea.bfs(ga.graph, (0, 0), (5, 0))
        self.assertEqual(score, None)

    def test_bfs_should_return_list_of_one_element_when_start_and_end_point_are_the_same(self):
        ga = prepare_gamearea.PrepareGamearea(1, 1)
        score = prepare_gamearea.bfs(ga.graph, (0, 0), (0, 0))
        self.assertEqual(len(score), 1)

    def test_bfs_should_return_the_shortest_way_for_full_graph(self):
        ga = prepare_gamearea.PrepareGamearea(5, 5)
        score = prepare_gamearea.bfs(ga.graph, (1, 1), (2, 2))
        self.assertEqual(len(score), 3)

    def test_bfs_should_return_none_when_we_try_to_connect_with_border_field(self):
        ga = prepare_gamearea.PrepareGamearea(5, 5)
        score = prepare_gamearea.bfs(ga.graph, (1, 1), (4, 4))
        self.assertEqual(score, None)

    def test_bfs_should_return_none_when_path_not_exists(self):
        ga = {}
        score = prepare_gamearea.bfs(ga, (1, 1), (4, 4))
        self.assertEqual(score, None)

    def test_check_if_path_exists_should_return_false_when_graph_is_empty(self):
        ga = {}
        score = prepare_gamearea.check_if_path_exists(ga, (0, 0), (1, 1))
        self.assertFalse(score)

    def test_check_if_path_exists_should_return_false_when_try_to_connect_with_border_field(self):
        ga = prepare_gamearea.PrepareGamearea(5, 5)
        score = prepare_gamearea.bfs(ga.graph, (1, 1), (4, 4))
        self.assertFalse(score)

    def test_check_if_path_exists_should_return_true_when_path_exists(self):
        ga = prepare_gamearea.PrepareGamearea(5, 5)
        score = prepare_gamearea.bfs(ga.graph, (1, 1), (3, 3))
        self.assertTrue(score)

    def prepare_gamearea_should_set_correct_number_of_rows(self):
        ga = prepare_gamearea.PrepareGamearea(5, 5)
        self.assertEqual(ga.number_of_rows, 5)

    def test_prepare_gamearea_should_set_correct_number_of_columns(self):
        ga = prepare_gamearea.PrepareGamearea(5, 5)
        self.assertEqual(ga.number_of_columns, 5)

    def test_init_of_prepare_gamearea_should_create_table_of_correct_number_of_rows(self):
        ga = prepare_gamearea.PrepareGamearea(3, 3)
        self.assertEqual(len(ga.table), 3)

    def test_init_of_prepare_gamearea_should_create_table_of_correct_number_of_columns(self):
        ga = prepare_gamearea.PrepareGamearea(4, 4)
        self.assertEqual(len(ga.table), 4)

    def test_init_of_prepare_gamearea_should_create_empty_graph_for_zeros_parameteres(self):
        ga = prepare_gamearea.PrepareGamearea(0, 0)
        self.assertEqual(len(ga.graph), 0)

    def test_prepare_gamearea_should_ignore_border_nodes(self):
        ga = prepare_gamearea.PrepareGamearea(3, 3)
        tmp = {(1, 1): []}
        self.assertEqual(ga.graph, tmp)

    def test_prepare_gamearea_should_create_correct_graph_for_small_board(self):
        ga = prepare_gamearea.PrepareGamearea(4, 4)
        tmp = {(1, 1): [(2, 1), (1, 2)],
               (1, 2): [(2, 2), (1, 1)],
               (2, 1): [(1, 1), (2, 2)],
               (2, 2): [(1, 2), (2, 1)]}
        self.assertEqual(ga.graph, tmp)

    def test_prepare_list_of_special_fields_should_be_empty_for_empty_board(self):
        ga = prepare_gamearea.PrepareGamearea(0, 0)
        list = ga.prepare_list_of_special_fields()
        self.assertEqual(list, [])

    def test_prepare_list_of_special_fields_should_not_containa_fields_closest_to_player(self):
        ga = prepare_gamearea.PrepareGamearea(5, 5)
        list = ga.prepare_list_of_special_fields()
        flag = False
        if (1, 1) in list:
            flag = True
        if (2, 1) in list:
            flag = True
        if (1, 2) in list:
            flag = True
        self.assertFalse(flag)

    def test_prepare_list_of_special_fields_should_not_containa_fields_closest_to_enemy(self):
        ga = prepare_gamearea.PrepareGamearea(5, 5)
        list = ga.prepare_list_of_special_fields()
        flag = False
        if (ga.number_of_rows - 2, ga.number_of_columns - 2) in list:
            flag = True
        if (ga.number_of_rows - 3, ga.number_of_columns - 2) in list:
            flag = True
        if (ga.number_of_rows - 2, ga.number_of_columns - 3) in list:
            flag = True
        self.assertFalse(flag)

    def test_prepare_should_return_correct_list_for_small_area(self):
        ga = prepare_gamearea.PrepareGamearea(5, 5)
        list = sorted(ga.prepare_list_of_special_fields())
        tmp = [(1, 3), (2, 2), (3, 1)]
        self.assertEqual(tmp, list)

    def test_prepare_should_return_correct_list_for_bigger_area(self):
        ga = prepare_gamearea.PrepareGamearea(7, 7)
        list = sorted(ga.prepare_list_of_special_fields())
        tmp = [(1, 3), (1, 4), (1, 5),
               (2, 2), (2, 3), (2, 4), (2, 5),
               (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
               (4, 1), (4, 2), (4, 3), (4, 4),
               (5, 1), (5, 2), (5, 3)]
        self.assertEqual(tmp, list)

    def test_before_set_door_field_position_of_door_should_be_minus_one(self):
        ga = prepare_gamearea.PrepareGamearea(5, 5)
        self.assertEqual((-1, -1), (ga.door_field_x, ga.door_field_y))

    def test_after_set_door_field_position_of_door_should_not_be_minus_one(self):
        ga = prepare_gamearea.PrepareGamearea(5, 5)
        ga.set_door_field(ga.prepare_list_of_special_fields())
        self.assertNotEqual((-1, -1), (ga.door_field_x,
                                       ga.door_field_y))

    def test_after_set_door_field_on_certain_position_in_table_should_be_value_three(self):
        ga = prepare_gamearea.PrepareGamearea(5, 5)
        ga.set_door_field(ga.prepare_list_of_special_fields())
        self.assertEqual(ga.table[ga.door_field_x][ga.door_field_y], 3)

    def test_create_table_of_game_should_not_be_empty(self):
        ga = prepare_gamearea.PrepareGamearea(5, 5)
        arr = ga.create_table_of_game()
        self.assertTrue(isinstance(arr, list))

    def test_create_table_should_have_value_of_three_where_door_is_placed(self):
        ga = prepare_gamearea.PrepareGamearea(9, 9)
        arr = ga.create_table_of_game()
        x = ga.door_field_x
        y = ga.door_field_y
        self.assertEqual(arr[x][y], 3)

    def test_set_fields_should_return_list(self):
        ga = prepare_gamearea.PrepareGamearea(5, 5)
        arr = ga.set_fields(3, [(1, 1), (1, 2), (2, 2)], 2)
        self.assertTrue(isinstance(arr, list))

    def test_set_fields_should_return_shorter_list_when_fields_were_added(self):
        ga = prepare_gamearea.PrepareGamearea(5, 5)
        arr = ga.set_fields(3, [(1, 1), (1, 2), (2, 2)], 2)
        self.assertLess(len(arr), 3)

    def test_set_fields_should_return_the_same_list_when_fields_were_not_added(self):
        ga = prepare_gamearea.PrepareGamearea(5, 5)
        arr = ga.set_fields(0, [(1, 1), (1, 2), (2, 2)], 2)
        self.assertEqual(arr, [(1, 1), (1, 2), (2, 2)])

    def test_set_fields_without_checking_path_should_return_list(self):
        ga = prepare_gamearea.PrepareGamearea(5, 5)
        arr = ga.set_fields_without_checking_path(3, [(1, 1), (1, 2), (2, 2)], 2)
        self.assertTrue(isinstance(arr, list))

    def test_set_fields_without_checking_path_should_return_shorter_list_when_fields_were_added(self):
        ga = prepare_gamearea.PrepareGamearea(5, 5)
        arr = ga.set_fields_without_checking_path(3, [(1, 1), (1, 2), (2, 2)], 2)
        self.assertLess(len(arr), 3)

    def test_set_fields_without_checking_path_should_return_the_same_list_when_fields_were_not_added(self):
        ga = prepare_gamearea.PrepareGamearea(5, 5)
        arr = ga.set_fields_without_checking_path(0, [(1, 1), (1, 2), (2, 2)], 2)
        self.assertEqual(arr, [(1, 1), (1, 2), (2, 2)])


suite = unittest.TestLoader().loadTestsFromTestCase(prepare_gamearea_tests)
print(unittest.TextTestRunner(verbosity=3).run(suite))
