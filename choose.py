import random

from treasure import Spell, Weapon, HealthPotion, ManaPotion


def choose_random_spell_from_file():
    try:
        with open('spells.txt', 'r') as f:
            spells_in_file = f.read().splitlines()
            spell_args_string = random.choice(spells_in_file)
            if spell_args_string == 'None':                   
                return None
            args = spell_args_string.split(',')
            spell = Spell(name=args[0], damage=int(args[1]), mana_cost=int(args[2]), cast_range=int(args[3]))               
            return spell
    except Exception as e:
       print(e)

def choose_random_weapon_from_file():
    try:
        with open('weapons.txt', 'r') as f:
            weapons_in_file = f.read().splitlines()
            weapon_args_string = random.choice(weapons_in_file)
            if weapon_args_string == 'None':                   
                return None
            args = weapon_args_string.split(',')
            weapon = Weapon(name=args[0], damage=int(args[1]))               
            return weapon
    except Exception as e:
       print(e)


def choose_random_treasure_from_file(file=None):
    if not file:
        file = "test_treasures.txt"
    try:
        with open(file, 'r') as f:
            treasures_in_file = f.read().splitlines()
            treasure_args_string = random.choice(treasures_in_file)
            if treasure_args_string == 'None':
                return None
            args = treasure_args_string.split(',')
            if args[0] == 'Spell':
                treasure = Spell(name=args[1], damage=int(args[2]),
                                 mana_cost=int(args[3]),
                                 cast_range=int(args[4]))
            elif args[0] == 'Weapon':
                treasure = Weapon(name=args[1], damage=int(args[2]))
            elif args[0] == 'HealthPotion':
                treasure = HealthPotion(name=args[1], healing=args[2])
            elif args[0] == 'ManaPotion':
                treasure = ManaPotion(name=args[1], mana_regen=args[2])
            return treasure
    except Exception as e:
        print(e)
