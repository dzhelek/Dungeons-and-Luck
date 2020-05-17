import unittest
from playable import Playable
from treasure import Spell, Weapon
from constants import PLAYER_ATTACK_BY_WEAPON_STRING, PLAYER_ATTACK_BY_SPELL_STRING

class Player(Playable):
	def __init__(self, health, mana):
		self.health = health
		self.mana = mana
		self.spell = None
		self.weapon = None

class TestPLayable(unittest.TestCase):
	#get_health()
	def test_get_health_with_given_player_should_return_health(self):
		pl = Player(health=100, mana=100)

		result = pl.get_health()
		expected = 100

		self.assertEqual(expected, result)

	#get_mana()
	def test_get_mana_with_given_player_should_return_mana(self):
		pl = Player(health=100, mana=50)

		result = pl.get_mana()
		expected = 50

		self.assertEqual(expected, result)

	#is_alive()
	def test_is_alive_with_given_alive_player_should_return_true(self):
		pl = Player(health=100, mana=50)

		result = pl.is_alive()
		expected = True

		self.assertEqual(expected, result)

	def test_is_alive_with_given_dead_player_should_return_false(self):
		pl = Player(health=0, mana=50)

		result = pl.is_alive()
		expected = False

		self.assertEqual(expected, result)

	#take_healing(healing_points)
	def test_take_healing_with_given_dead_player_should_return_false(self):
		pl = Player(health=0, mana=50)

		result = pl.take_healing(healing_points=20)
		expected = False

		self.assertEqual(expected, result)
		self.assertEqual(0, pl.health)

	def test_take_healing_with_given_alive_player_with_max_health_should_not_change_health_and_return_true(self):
		pl = Player(health=100, mana=50)

		result = pl.take_healing(healing_points=20)
		expected = True

		self.assertEqual(expected, result)
		self.assertEqual(100, pl.health)

	def test_take_healing_with_given_alive_player_with_less_than_max_health_should_change_health_and_return_true(self):
		pl = Player(health=90, mana=50)

		result = pl.take_healing(healing_points=20)
		expected = True

		self.assertEqual(expected, result)
		self.assertEqual(100, pl.health)

	#take_damage(damage_points)
	def test_with_given_dead_player_should_do_nothing(self):
		pl = Player(health=0, mana=50)

		pl.take_damage(damage_points=20)

		self.assertEqual(0, pl.health)

	def test_with_given_alive_player_and_points_more_than_health_should_change_health_to_zero(self):
		pl = Player(health=10, mana=50)

		pl.take_damage(damage_points=20)

		self.assertEqual(0, pl.health)

	def test_with_given_alive_player_and_points_less_than_health_should_change_health_to_difference_between_health_and_damage(self):
		pl = Player(health=30, mana=50)

		pl.take_damage(damage_points=20.2)

		self.assertEqual(9.8, pl.health)

	#take_mana(mana_points):
	def test_with_given_player_should_add_mana_points_to_mana(self):
		pl = Player(health=100, mana=50)

		pl.take_mana(mana_points=120)

		self.assertEqual(100, pl.mana)

	#equip(weapon)
	def test_equip_with_given_player_and_invalid_weapon_as_argument_should_raise_exception(self):
		pl = Player(health=100, mana=60)
		weapon = 'weapon'
		
		exc = None
		try:		
			result = pl.equip(weapon=weapon)
		except Exception as e:
			exc = e

		self.assertEqual(str(exc), 'Invalid weapon given for equipment')
		self.assertEqual(None, pl.weapon)	

	def test_equip_with_given_player_and_valid_weapon_as_argument_should_set_weapon(self):
		pl = Player(health=100, mana=60)
		weapon = Weapon(name='Fireball', damage=30)		
				
		pl.equip(weapon=weapon)
		
		self.assertEqual(weapon, pl.weapon)	

	#learn(spell)
	def test_learn_with_given_player_and_invalid_spell_as_argument_should_raise_exception(self):
		pl = Player(health=100, mana=60)
		spell = Weapon(name='Fireball', damage=30)	
		
		exc = None
		try:		
			result = pl.learn(spell=spell)
		except Exception as e:
			exc = e

		self.assertEqual(str(exc), 'Invalid spell given for learning')
		self.assertEqual(None, pl.spell)	

	def test_learn_with_given_player_with_no_spell_and_valid_spell_as_argument_should_set_spell(self):
		pl = Player(health=100, mana=60)
		spell = Spell(name='Fireball', damage=30, mana_cost=50, cast_range=2)
				
		pl.learn(spell=spell)
		
		self.assertEqual(spell, pl.spell)	

	def test_learn_with_given_player_with_spell_and_valid_spell_as_argument_should_change_spell(self):
		pl = Player(health=100, mana=60)
		spell = Spell(name='Fireball', damage=30, mana_cost=50, cast_range=2)
		pl.learn(spell=spell)

		new_spell = Spell(name='New spell', damage=30, mana_cost=50, cast_range=2)
		pl.learn(new_spell)
		
		self.assertEqual(new_spell, pl.spell)	

	

	#can_cast():
	# def test_with_given_player_and_no_spell_should_raise_exception(self):
	# 	pl = Player(health=100, mana=50)

	# 	exc = None
	# 	try:
	# 		result = pl.can_cast()
	# 	except Exception as e:
	# 		exc = e

	# 	self.assertIsNotNone(exc)
	# 	self.assertEqual(str(exc), 'No spell to cast')

	# def test_with_given_player_and_spell_with_mana_cost_more_than_players_mana_should_raise_exception(self):
	# 	pl = Player(health=100, mana=49)
	# 	spell = Spell(name='Fireball', damage=30, mana_cost=50, cast_range=2)
	# 	pl.spell = spell

	# 	exc = None
	# 	try:
	# 		result = pl.can_cast()
	# 	except Exception as e:
	# 		exc = e

	# 	self.assertIsNotNone(exc)
	# 	self.assertEqual(str(exc), 'Not enough mana to cast spell')

	def test_with_given_player_and_no_spell_should_return_False(self):
		pl = Player(health=100, mana=50)

		result = pl.can_cast()
		
		self.assertEqual(False, result)

	def test_with_given_player_and_spell_with_mana_cost_more_than_players_mana_should_return_False(self):
		pl = Player(health=100, mana=49)
		spell = Spell(name='Fireball', damage=30, mana_cost=50, cast_range=2)
		pl.learn(spell)
		
		result = pl.can_cast()
		
		self.assertEqual(False, result)

	def test_with_given_player_and_spell_with_mana_cost_less_than_player_mana_should_lower_players_mana_and_return_True(self):
		pl = Player(health=100, mana=60)
		spell = Spell(name='Fireball', damage=30, mana_cost=50, cast_range=2)
		pl.learn(spell)
		
		result = pl.can_cast()

		self.assertEqual(True, result)		

	#attack(by)
	def test_with_given_player_and_invalid_by_as_argument_should_raise_exception(self):
		pl = Player(health=100, mana=50)
		by = None

		exc = None
		try:
			pl.attack(by=by)
		except Exception as e:
			exc = e

		self.assertIsNotNone(exc)
		self.assertEqual(str(exc), 'Invalid item for attack given')

	def test_with_given_player_with_no_weapon_and_weapon_as_argument_should_return_zero(self):
		pl = Player(health=100, mana=50)
		by = PLAYER_ATTACK_BY_WEAPON_STRING
		
		result = pl.attack(by=by)
		
		self.assertEqual(0, result)

	def test_with_given_player_with_weapon_and_weapon_as_argument_should_return_damage_of_weapon(self):
		pl = Player(health=100, mana=50)
		weapon = Weapon(name='Fireball', damage=30)	
		pl.equip(weapon)
		by = PLAYER_ATTACK_BY_WEAPON_STRING
		
		result = pl.attack(by=by)
		
		self.assertEqual(30, result)

	def test_with_given_player_with_no_spell_and_spell_as_argument_should_return_zero(self):
		pl = Player(health=100, mana=50)
		by = PLAYER_ATTACK_BY_SPELL_STRING
		
		result = pl.attack(by=by)
		
		self.assertEqual(0, result)

	def test_with_given_player_with_castable_spell_and_spell_as_argument_should_return_damage_of_spell(self):
		pl = Player(health=100, mana=50)
		spell = Spell(name='Fireball', damage=30, mana_cost=50, cast_range=2)
		pl.learn(spell)
		by = PLAYER_ATTACK_BY_SPELL_STRING
		
		result = pl.attack(by=by)
		
		self.assertEqual(30, result)

	def test_with_given_player_with_non_castable_spell_and_spell_as_argument_should_return_zerol(self):
		pl = Player(health=100, mana=20)
		spell = Spell(name='Fireball', damage=30, mana_cost=50, cast_range=2)
		pl.learn(spell)
		by = PLAYER_ATTACK_BY_SPELL_STRING
		
		result = pl.attack(by=by)
		
		self.assertEqual(0, result)



if __name__ == '__main__':
	unittest.main()