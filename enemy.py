import random

from choose import (choose_random_spell_from_file,
                    choose_random_weapon_from_file)
from playable import Playable


class Enemy(Playable):
    def __init__(self):
        self.health = random.randint(50, 100)
        self.mana = random.randint(50, 100)
        self.damage = random.randint(10, 50)
        self.weapon = choose_random_weapon_from_file()
        self.spell = choose_random_spell_from_file()

    def __repr__(self):
        return "Enemy(health={h},\
 mana={m}, damage={d})".format(h=self.health, m=self.mana, d=self.damage)

    def attack(self, **kwargs):
        result_from_attack = None
        try:
            result_from_attack = super().attack(**kwargs)
        except Exception as e:
            raise e
        if result_from_attack is not None:
            return result_from_attack
        return self.damage
