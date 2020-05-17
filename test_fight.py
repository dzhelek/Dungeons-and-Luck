import unittest

from constants import (PLAYER_ATTACK_BY_WEAPON_STRING,)
from enemy import Enemy
from fight import Fight, flip_direction
from hero import Hero
from treasure import Weapon, Spell


class TestFlipDirection(unittest.TestCase):
    def test_with_right_returns_left(self):
        self.assertEqual('left', flip_direction('right'))

    def test_with_left_returns_right(self):
        self.assertEqual('right', flip_direction('left'))

    def test_with_up_returns_down(self):
        self.assertEqual('up', flip_direction('down'))

    def test_with_down_returns_up(self):
        self.assertEqual('down', flip_direction('up'))

    def test_with_zero_returns_zero(self):
        self.assertEqual(0, flip_direction(0))


# tests with mana are not valid because tha mana changes
class TestFight(unittest.TestCase):
    def test_init_fiht(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        e = Enemy()

        f = Fight(h, e)

        self.assertIsNotNone(f)
        self.assertIsNotNone(f.hero)
        self.assertIsNotNone(f.enemy)

    def test_validate_fight(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)

        with self.assertRaises(AssertionError):
            Fight(h, 1)
        with self.assertRaises(AssertionError):
            Fight(0, Enemy())

    def test_with_weapon_should_attack_by_weapon(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        h.equip(Weapon(name="The Axe of Destiny", damage=20))
        e = Enemy()

        Fight(h, e)

        self.assertEqual(h.attacking, PLAYER_ATTACK_BY_WEAPON_STRING)

    # def test_with_spell_should_attack_by_spell(self):
    #     h = Hero(name="Bron", title="Dragonslayer",
    #              health=100, mana=100, mana_regeneration_rate=2)
    #     h.learn(Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2))
    #     e = Enemy()

    #     Fight(h, e)

    #     self.assertEqual(h.attacking, PLAYER_ATTACK_BY_SPELL_STRING)

    # def test_with_spell_and_weapon_should_attack_by_higher_damage(self):
    #     h = Hero(name="Bron", title="Dragonslayer",
    #              health=100, mana=100, mana_regeneration_rate=2)
    #     h.learn(Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2))
    #     h.equip(Weapon(name="The Axe of Destiny", damage=20))
    #     e = Enemy()

    #     Fight(h, e)

    #     self.assertEqual(h.attacking, PLAYER_ATTACK_BY_SPELL_STRING)

    def test_with_weapon_and_spell_should_attack_by_higher_damage(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        h.learn(Spell(name="Fireball", damage=20, mana_cost=50, cast_range=2))
        h.equip(Weapon(name="The Axe of Destiny", damage=30))
        e = Enemy()

        Fight(h, e)

        self.assertEqual(h.attacking, PLAYER_ATTACK_BY_WEAPON_STRING)

    # def test_with_equal_spell_and_weapon_damage_should_attack_by_spell(self):
    #     h = Hero(name="Bron", title="Dragonslayer",
    #              health=100, mana=100, mana_regeneration_rate=2)
    #     h.learn(Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2))
    #     h.equip(Weapon(name="The Axe of Destiny", damage=30))
    #     e = Enemy()

    #     Fight(h, e)

    #     self.assertEqual(h.attacking, PLAYER_ATTACK_BY_SPELL_STRING)

    def test_with_spell_and_weapon_but_no_mana_should_attack_by_weapon(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        h.learn(Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2))
        h.equip(Weapon(name="The Axe of Destiny", damage=20))
        e = Enemy()
        h.mana = 0

        Fight(h, e)

        self.assertEqual(h.attacking, PLAYER_ATTACK_BY_WEAPON_STRING)

    # def test_with_spell_and_weapon_with_distance_should_attack_by_spell(self):
    #     h = Hero(name="Bron", title="Dragonslayer",
    #              health=100, mana=100, mana_regeneration_rate=2)
    #     h.learn(Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2))
    #     h.equip(Weapon(name="The Axe of Destiny", damage=40))
    #     e = Enemy()

    #     Fight(h, e, distance=2)

    #     self.assertEqual(h.attacking, PLAYER_ATTACK_BY_SPELL_STRING)

    def test_with_spell_and_weapon_with_distance_and_no_mana_should_move(self):
        h = Hero(name="Bron", title="Dragonslayer",
                 health=100, mana=100, mana_regeneration_rate=2)
        h.learn(Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2))
        h.equip(Weapon(name="The Axe of Destiny", damage=40))
        e = Enemy()
        h.mana = 0

        f = Fight(h, e, distance=2)

        self.assertEqual(f.distance, 0)


if __name__ == '__main__':
    unittest.main()
