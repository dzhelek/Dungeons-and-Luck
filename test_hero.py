import unittest
from constants import PLAYER_ATTACK_BY_WEAPON_STRING, PLAYER_ATTACK_BY_SPELL_STRING
from hero import Hero
from treasure import Spell, Weapon

class TestHero(unittest.TestCase):
	#__init__()
	def test_with_given_correct_arguments_should_initialise_hero(self):
		name = 'Bron'
		title = 'Dragonslayer'
		health = 100
		mana = 100
		mana_regeneration_rate = 2

		h = Hero(name, title, health, mana, mana_regeneration_rate)

		self.assertEqual(Hero, type(h))
		self.assertEqual(name, h.name)
		self.assertEqual(title, h.title)
		self.assertEqual(health, h.health)
		self.assertEqual(mana, h.mana)
		self.assertEqual(mana_regeneration_rate, h.mana_regeneration_rate)

	#known_as()
	def test_with_given_hero_should_return_correctly(self):
		name = 'Bron'
		title = 'Dragonslayer'
		health = 100
		mana = 100
		mana_regeneration_rate = 2
		h = Hero(name, title, health, mana, mana_regeneration_rate)

		result = h.known_as()
		expected = name + ' the ' + title

		self.assertEqual(expected, result)

	#attack(by)
	def test_with_given_hero_and_invalid_by_as_argument_should_raise_exception(self):
		name = 'Bron'
		title = 'Dragonslayer'
		health = 100
		mana = 100
		mana_regeneration_rate = 2
		h = Hero(name, title, health, mana, mana_regeneration_rate)
		by = None

		exc = None
		try:
			h.attack(by=by)
		except Exception as e:
			exc = e

		self.assertIsNotNone(exc)
		self.assertEqual(str(exc), 'Invalid item for attack given')

	def test_with_given_hero_with_no_weapon_and_weapon_as_argument_should_return_zero(self):
		name = 'Bron'
		title = 'Dragonslayer'
		health = 100
		mana = 100
		mana_regeneration_rate = 2
		h = Hero(name, title, health, mana, mana_regeneration_rate)
		by = PLAYER_ATTACK_BY_WEAPON_STRING
		
		result = h.attack(by=by)
		
		self.assertEqual(0, result)

	def test_with_given_hero_with_weapon_and_weapon_as_argument_should_return_damage_of_weapon(self):
		name = 'Bron'
		title = 'Dragonslayer'
		health = 100
		mana = 100
		mana_regeneration_rate = 2
		h = Hero(name, title, health, mana, mana_regeneration_rate)
		weapon = Weapon(name='Fireball', damage=30)	
		h.equip(weapon)
		by = PLAYER_ATTACK_BY_WEAPON_STRING
		
		result = h.attack(by=by)
		
		self.assertEqual(30, result)

	def test_with_given_hero_with_no_spell_and_spell_as_argument_should_return_zero(self):
		name = 'Bron'
		title = 'Dragonslayer'
		health = 100
		mana = 100
		mana_regeneration_rate = 2
		h = Hero(name, title, health, mana, mana_regeneration_rate)
		by = PLAYER_ATTACK_BY_SPELL_STRING
		
		result = h.attack(by=by)
		
		self.assertEqual(0, result)

	def test_with_given_hero_with_castable_spell_and_spell_as_argument_should_return_damage_of_spell(self):
		name = 'Bron'
		title = 'Dragonslayer'
		health = 100
		mana = 100
		mana_regeneration_rate = 2
		h = Hero(name, title, health, mana, mana_regeneration_rate)
		spell = Spell(name='Fireball', damage=30, mana_cost=50, cast_range=2)
		h.learn(spell)
		by = PLAYER_ATTACK_BY_SPELL_STRING
		
		result = h.attack(by=by)
		
		self.assertEqual(30, result)

	def test_with_given_hero_with_non_castable_spell_and_spell_as_argument_should_return_zerol(self):
		name = 'Bron'
		title = 'Dragonslayer'
		health = 100
		mana = 20
		mana_regeneration_rate = 2
		h = Hero(name, title, health, mana, mana_regeneration_rate)
		spell = Spell(name='Fireball', damage=30, mana_cost=50, cast_range=2)
		h.learn(spell)
		by = PLAYER_ATTACK_BY_SPELL_STRING
		
		result = h.attack(by=by)
		
		self.assertEqual(0, result)

	def test_with_given_hero_and_no_item_for_attack_should_return_zero(self):
		name = 'Bron'
		title = 'Dragonslayer'
		health = 100
		mana = 100
		mana_regeneration_rate = 2
		h = Hero(name, title, health, mana, mana_regeneration_rate)
		
		result = h.attack()
		
		self.assertEqual(0, result)

if __name__ == '__main__':
	unittest.main()