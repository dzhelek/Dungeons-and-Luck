import unittest

from treasure import Treasure, Weapon, Spell

# class TestTreasure(unittest.TestCase):
#     def test_init_treasure(self):
#         t = Treasure.get_random_treasure()

#         self.assertIsInstance(t, Treasure)


class TestWeapon(unittest.TestCase):
    def test_init_weapon(self):
        name = "The Axe of Destiny"
        damage = 20

        w = Weapon(name=name, damage=damage)

        self.assertEqual(w.name, name)
        self.assertEqual(w.damage, damage)


class TestSpell(unittest.TestCase):
    def test_init_spell(self):
        name = "Fireball"
        damage = 30
        mana_cost = 50
        cast_range = 50

        s = Spell(name=name, damage=damage,\
         mana_cost=mana_cost, cast_range=cast_range)

        self.assertEqual(s.name, name)
        self.assertEqual(s.damage, damage)
        self.assertEqual(s.mana_cost, mana_cost)
        self.assertEqual(s.cast_range, cast_range)


if __name__ == '__main__':
    unittest.main()
