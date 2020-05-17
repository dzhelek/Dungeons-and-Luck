import unittest

from constants import PLAYER_ATTACK_BY_SPELL_STRING
from dungeon import Dungeon
from hero import Hero
from treasure import Spell


class TestDungeon(unittest.TestCase):
    def test_validate_map_with_correct_input(self):
        string = ('''S.##.....T
#T##..###.
#.###E###E
#.E...###.
###T#####G''')

        a = Dungeon.from_string(string)

        self.assertIsInstance(a, Dungeon)
        self.assertEqual(a.to_string("test.txt"), string)

    def test_validate_map_with_unequal_lengths_of_map_rows(self):
        string = ('''S.##.....T
#T##..###.
#.###E###
#.E...###.
###T#####G''')

        with self.assertRaises(AssertionError):
            Dungeon.from_string(string)

    def test_to_list(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''S.##.....T
#T##..###.
#.###E###E
#.E...###.
###T#####G''')
        a.spawn(h)
        expected = ([['H', '.', '#', '#', '.', '.', '.', '.', '.', 'T'],
                    ['#', 'T', '#', '#', '.', '.', '#', '#', '#', '.'],
                    ['#', '.', '#', '#', '#', 'E', '#', '#', '#', 'E'],
                    ['#', '.', 'E', '.', '.', '.', '#', '#', '#', '.'],
                    ['#', '#', '#', 'T', '#', '#', '#', '#', '#', 'G']])

        a.get_current_position()

        self.assertEqual(expected, a.list_map)

    def test_validate_map_with_no_starting_point_should_raise_error(self):
        with self.assertRaises(AssertionError):
            Dungeon.from_string('''T.##.....T
#T##..###.
#.###E###E
#.E...###.
###T#####G''')

    def test_validate_map_with_more_than_one_gates(self):
        with self.assertRaises(AssertionError):
            Dungeon.from_string('''S.##.....T
#G##..###.
#.###E###E
#.E...###.
###T#####G''')

    def test_spawn_hero_should_put_exactly_one_hero_on_the_map(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''S.##.....T
#T##..###.
#.###E###E
#.E...###.
###T#####G''')

        a.spawn(h)

        self.assertIn('H', a.map)

    def test_spawn_hero_with_no_more_spawning_points_should_return_false(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''S.##.....T
#T##..###.
#.###E###E
#.E...###.
###T#####G''')
        a.spawn(h)
        a.map = a.map.replace('H', 'T')

        spawned_successfully = a.spawn(h)

        self.assertFalse(spawned_successfully, "no starting points")

    def test_spawn_more_than_one_heroes_should_return_false(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''S.##.....T
#T##..###.
#.###E###E
#.E...###.
###T#####G''')
        a.spawn(h)

        spawned_successfully = a.spawn(h)

        self.assertFalse(spawned_successfully, "hero already spwaned!")

    def test_spawn_multiple_times(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''S.##....ST
#T##..###.
#.###E###E
#.E..S###.
###T#####G''')
        spawned_successfully1 = a.spawn(h)
        a.map = a.map.replace('H', 'T')
        spawned_successfully2 = a.spawn(h)
        a.map = a.map.replace('H', 'T')
        spawned_successfully3 = a.spawn(h)

        self.assertTrue(spawned_successfully1, "cannot spawn")
        self.assertTrue(spawned_successfully2, "cannot spawn")
        self.assertTrue(spawned_successfully3, "cannot spawn")

    def test_pick_treasure(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''S.##....ST
#T##..###.
#.###E###E
#.E..S###.
###T#####G''')
        a.spawn(h)

        treasure = a.pick_treasure()

        self.assertIsNotNone(treasure)

    def test_get_current_position_with_the_very_first(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''S.##.....T
#T##..###.
#.###E###E
#.E...###.
###T#####G''')
        a.spawn(h)

        current_position = a.get_current_position()

        self.assertEqual(current_position, (0, 0))

    def test_get_current_position_with_first_last(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''..##.....S
#T##..###.
#.###E###E
#.E...###.
###T#####G''')
        a.spawn(h)

        current_position = a.get_current_position()

        self.assertEqual(current_position, (9, 0))

    def test_get_current_position_with_last_last(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''..##......
#G##..###.
#.###E###E
#.E...###.
###T#####S''')
        a.spawn(h)

        current_position = a.get_current_position()

        self.assertEqual(current_position, (9, 4))

    def test_get_current_position_with_second_second(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''..##......
#S##..###.
#.###E###E
#.E...###.
###T#####G''')
        a.spawn(h)

        current_position = a.get_current_position()

        self.assertEqual(current_position, (1, 1))


class TestMoveHero(unittest.TestCase):
    def test_move_hero(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''S.##.....T
..##..###.
#.###E###E
#.E...###.
###T#####G''')
        a.spawn(h)

        moved_successfully = a.move_hero('right')

        self.assertTrue(moved_successfully, "cannot move")

    def test_move_hero_with_right_next_to_the_wall_should_return_false(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''T.##.....S
..##..###.
#.###E###E
#.E...###.
###T#####G''')
        a.spawn(h)

        moved_successfully = a.move_hero('right')

        self.assertFalse(moved_successfully, "got out of the map")

    def test_move_hero_with_right_should_move_the_hero(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''S.##.....T
..##..###.
#.###E###E
#.E...###.
###T#####G''')
        expected = ('''.H##.....T
..##..###.
#.###E###E
#.E...###.
###T#####G''')
        a.spawn(h)

        a.move_hero('right')

        self.assertEqual(expected, a.map)

    def test_move_hero_with_left_should_move_the_hero(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''S.##.....T
..##..###.
#.###E###E
#.E...###.
###T#####G''')
        expected = ('''H.##.....T
..##..###.
#.###E###E
#.E...###.
###T#####G''')
        a.spawn(h)
        a.move_hero('right')

        a.move_hero('left')

        self.assertEqual(expected, a.map)

    def test_move_hero_with_left_next_to_the_wall_should_return_false(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''S.##.....T
..##..###.
#.###E###E
#.E...###.
###T#####G''')
        a.spawn(h)

        moved_successfully = a.move_hero('left')

        self.assertFalse(moved_successfully, "got out of the map")

    def test_move_hero_with_up_should_move_the_hero(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''..##.....T
.S##..###.
#.###E###E
#.E...###.
###T#####G''')
        expected = ('''.H##.....T
..##..###.
#.###E###E
#.E...###.
###T#####G''')
        a.spawn(h)
        a.move_hero('left')
        a.move_hero('right')

        a.move_hero('up')

        self.assertEqual(expected, a.map)

    def test_move_hero_with_up_next_to_the_wall_should_return_false(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''S.##.....T
..##..###.
#.###E###E
#.E...###.
###T#####G''')
        a.spawn(h)

        moved_successfully = a.move_hero('up')

        self.assertFalse(moved_successfully, "got out of the map")

    def test_move_hero_with_down_should_move_the_hero(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''..##.....T
.S##..###.
#.###E###E
#.E...###.
###T#####G''')
        expected = ('''..##.....T
.H##..###.
#.###E###E
#.E...###.
###T#####G''')
        a.spawn(h)
        a.move_hero('left')
        a.move_hero('right')
        a.move_hero('up')

        a.move_hero('down')

        self.assertEqual(expected, a.map)

    def test_move_hero_with_down_next_to_the_wall_should_return_false(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''..##.....T
..##..###.
#.###E###E
#.ES..###.
###.#####G''')
        a.spawn(h)
        a.move_hero('down')

        moved_successfully = a.move_hero('down')

        self.assertFalse(moved_successfully, "got out of the map")

    def test_move_onto_an_obstacle_returns_false_but_others_true(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''..##.....T
..##..###.
#.###E###E
#.ES..###.
###.#####G''')
        a.spawn(h)

        moved_successfully1 = a.move_hero('down')
        moved_successfully2 = a.move_hero('right')
        moved_successfully3 = a.move_hero('left')
        moved_successfully4 = a.move_hero('up')
        moved_successfully5 = a.move_hero('right')
        moved_successfully6 = a.move_hero('right')
        moved_successfully7 = a.move_hero('right')

        self.assertTrue(moved_successfully1, "cannot move")
        self.assertFalse(moved_successfully2, "got onto an obstacle")
        self.assertFalse(moved_successfully3, "got onto an obstacle")
        self.assertTrue(moved_successfully4, "cannot move")
        self.assertTrue(moved_successfully5, "cannot move")
        self.assertTrue(moved_successfully6, "cannot move")
        self.assertFalse(moved_successfully7, "got onto an obstacle")

    def test_move_hero_with_unvalid_direction_returns_false(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''..##.....T
..##..###.
#.###E###E
#.ES..###.
###.#####G''')
        a.spawn(h)

        moved_successfully = a.move_hero('upleft')

        self.assertFalse(moved_successfully, "unvalid move direction")

    def test_move_onto_a_treasure_returns_true(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        a = Dungeon.from_string('''..##....ST
..##..###.
#.###E###E
#.E...###.
###.#####G''')
        a.spawn(h)

        moved_successfully = a.move_hero('right')

        self.assertTrue(moved_successfully, "cannot move onto a treasure")


class TestEnemyInCastingRange(unittest.TestCase):
    def test_with_right_with_enemy_behind_wall_returns_false(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        h.learn(Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2))
        a = Dungeon.from_string('''..##.....T
..##..###.
#.#S#E###E
#.E...###.
###.#####G''')
        a.spawn(h)

        result = a.enemy_in_casting_range('right')

        self.assertFalse(result, "attempt to attack through the wall")

    def test_with_left_with_enemy_behind_wall_returns_false(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        h.learn(Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2))
        a = Dungeon.from_string('''..##.....T
..##..###.
#.#.#E#S#E
#.E...###.
###.#####G''')
        a.spawn(h)

        result = a.enemy_in_casting_range('left')

        self.assertFalse(result, "attempt to attack through the wall")

    def test_with_up_with_enemy_behind_wall_returns_false(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        h.learn(Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2))
        a = Dungeon.from_string('''..##.....T
..##..###.
#.#.#E###E
#.E...####
###.##G##S''')
        a.spawn(h)

        result = a.enemy_in_casting_range('up')

        self.assertFalse(result, "attempt to attack through the wall")

    def test_with_down_with_enemy_behind_wall_returns_false(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        h.learn(Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2))
        a = Dungeon.from_string('''..##.....T
..S#..###.
#.#.#E###E
#.E...###.
###.#####G''')
        a.spawn(h)

        result = a.enemy_in_casting_range('down')

        self.assertFalse(result, "attempt to attack through the wall")

    def test_with_right_with_enemy_in_spell_range_returns_true(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        h.learn(Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2))
        a = Dungeon.from_string('''..##.....T
..##..###.
#.#S.E###E
#.E...###.
###.#####G''')
        a.spawn(h)

        result = a.enemy_in_casting_range('right')

        self.assertTrue(result, "cannot attack right")

    def test_with_left_with_enemy_in_spell_range_returns_true(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        h.learn(Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2))
        a = Dungeon.from_string('''..##.....T
..##..###.
#.#..E###E
#.E.S.###.
###.#####G''')
        a.spawn(h)

        result = a.enemy_in_casting_range('left')

        self.assertTrue(result, "cannot attack left")

    def test_with_up_with_enemy_in_spell_range_returns_true(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        h.learn(Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2))
        a = Dungeon.from_string('''..##.....T
..##..###.
#.#.E###E.
#.E...###.
##S.#####G''')
        a.spawn(h)

        result = a.enemy_in_casting_range('up')

        self.assertTrue(result, "cannot attack up")

    def test_with_down_with_enemy_in_spell_range_returns_true(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        h.learn(Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2))
        a = Dungeon.from_string('''..##.....T
..##..###.
#.S.E###E.
#.E...###.
##..#####G''')
        a.spawn(h)

        result = a.enemy_in_casting_range('down')

        self.assertTrue(result, "cannot attack down")

    def test_with_unvalid_direction_returns_false(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        h.learn(Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2))
        a = Dungeon.from_string('''..##.....T
..##..###.
#.S.E###E.
#.E...###.
##..#####G''')
        a.spawn(h)

        result = a.enemy_in_casting_range('downleft')

        self.assertFalse(result, "unvalid direction")

    def test_by_spell_with_no_enemy_in_casting_range(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        h.learn(Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2))
        a = Dungeon.from_string('''..##.....T
.S##..###.
#.###E###E
#.E...###.
###.#####G''')
        a.spawn(h)

        attack = a.hero_attack(by=PLAYER_ATTACK_BY_SPELL_STRING, direction='down')

        self.assertEqual(attack, "Nothing in casting range 2")


if __name__ == '__main__':
    unittest.main()
