import unittest

from choose import choose_random_spell_from_file, choose_random_weapon_from_file
from constants import PLAYER_ATTACK_BY_WEAPON_STRING, PLAYER_ATTACK_BY_SPELL_STRING
from enemy import Enemy
from treasure import Spell, Weapon

class TestEnemy(unittest.TestCase):
	#__init__()
	def test_with_given_no_arguments_should_initialise_enemy(self):
		e = Enemy()

		self.assertEqual(Enemy, type(e))
		self.assertTrue(hasattr(e, 'health'))
		self.assertTrue(hasattr(e, 'mana'))
		self.assertTrue(hasattr(e, 'damage'))
		self.assertTrue(hasattr(e, 'spell'))
		self.assertTrue(hasattr(e, 'weapon'))

	#attack(by)
	def test_with_given_enemy_and_invalid_by_as_argument_should_raise_exception(self):
		e = Enemy()
		by = None

		exc = None
		try:
			e.attack(by=by)
		except Exception as e:
			exc = e

		self.assertIsNotNone(exc)
		self.assertEqual(str(exc), 'Invalid item for attack given')

	def test_attack_by_weapon_with_given_enemy_should_return_correct_value(self):
		e = Enemy()
		by = PLAYER_ATTACK_BY_WEAPON_STRING

		result = e.attack(by=by)

		if e.weapon == None:
			self.assertEqual(0, result)
		else:
			self.assertEqual(e.weapon.damage, result)

	def test_attack_by_spell_with_given_enemy_should_return_correct_value(self):
		e = Enemy()
		by = PLAYER_ATTACK_BY_SPELL_STRING

		enemy_mana_before_attack = e.mana
			
		result = e.attack(by=by)

		
		if e.spell == None:		
			self.assertEqual(0, result)
		else:
			if e.spell.mana_cost > enemy_mana_before_attack:
				self.assertEqual(0, result)
			else:
				self.assertEqual(e.spell.damage, result)


	def test_with_given_enemy_with_no_item_for_attack_should_return_damage_of_enemy(self):
		e = Enemy()		
			
		result = e.attack()

		self.assertEqual(e.damage, result)

if __name__ == '__main__':
	unittest.main()