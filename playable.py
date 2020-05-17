from constants import (PLAYER_MAX_MANA_AND_HEALTH,
                       PLAYER_MIN_MANA_AND_HEALTH,
                       PLAYER_ATTACK_BY_WEAPON_STRING,
                       PLAYER_ATTACK_BY_SPELL_STRING)
from treasure import Spell, Weapon


def regulate_player_attribute(attribute):
    if attribute < PLAYER_MIN_MANA_AND_HEALTH:
        return PLAYER_MIN_MANA_AND_HEALTH
    elif attribute > PLAYER_MAX_MANA_AND_HEALTH:
        return PLAYER_MAX_MANA_AND_HEALTH
    return attribute


class Playable:
    def get_health(self):
        return self.health

    def get_mana(self):
        return self.mana

    def is_alive(self):
        return self.health > 0

    def take_healing(self, healing_points):
        if self.is_alive():
            self.health += healing_points
            self.health = regulate_player_attribute(attribute=self.health)
            return True
        return False

    def take_damage(self, damage_points):
        self.health -= damage_points
        self.health = regulate_player_attribute(attribute=self.health)

    def take_mana(self, mana_points):
        self.mana += mana_points
        self.mana = regulate_player_attribute(attribute=self.mana)

    def equip(self, weapon):
        if type(weapon) != Weapon:
            raise ValueError('Invalid weapon given for equipment')
        self.weapon = weapon

    def learn(self, spell):
        if type(spell) != Spell:
            raise ValueError('Invalid spell given for learning')
        self.spell = spell

    def can_cast(self):
        if self.spell is None:
            return False
        if self.spell.mana_cost > self.mana:
            return False
        return True

    def attack(self, **kwargs):
        if 'by' in kwargs.keys():
            if kwargs['by'] == PLAYER_ATTACK_BY_WEAPON_STRING:
                if self.weapon is not None:
                    return self.weapon.damage
                else:
                    return 0
            elif kwargs['by'] == PLAYER_ATTACK_BY_SPELL_STRING:
                if self.can_cast():
                    self.mana -= self.spell.mana_cost
                    self.mana = regulate_player_attribute(attribute=self.mana)
                    return self.spell.damage
                else:
                    return 0
            raise ValueError('Invalid item for attack given')
        else:
            return None
