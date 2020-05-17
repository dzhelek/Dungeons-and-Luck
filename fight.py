from constants import (PLAYER_ATTACK_BY_SPELL_STRING,
                       PLAYER_ATTACK_BY_WEAPON_STRING)
from enemy import Enemy
from hero import Hero
from playable import Playable
from treasure import Spell, Weapon


def flip_direction(direction):
        if direction:
            if direction == 'up':
                return 'down'
            elif direction == 'down':
                return 'up'
            elif direction == 'left':
                return 'right'
            elif direction == 'right':
                return 'left'
            else:
                raise ValueError
        else:
            return direction


class Fight:
    def __init__(self, hero, enemy, distance=0, direction=0):
        assert isinstance(hero, Playable)
        assert isinstance(enemy, Playable)

        self.hero = hero
        self.enemy = enemy
        self.distance = distance
        self.direction = direction
        self.opposite_direction = flip_direction(direction)

        self.hero.enough_mana = True
        self.enemy.enough_mana = True

        self.happened = 'A fight is started between our {h} and {e}\n'.format(h=self.hero, e=self.enemy)

        while True:
            self.hero_on_turn()
            if not self.enemy.is_alive():
                self.happened += 'Enemy is dead'
                break

            self.enemy_on_turn()
            if not self.hero.is_alive():
                self.happened += 'Hero is dead'
                break

    def __repr__(self):
        return self.happened

    def __str__(self):
        return self.happened

    def set_hero_attack(self):
        if not self.distance:
            if self.hero.can_cast():
                if self.hero.weapon:
                        if self.hero.spell.damage >= self.hero.weapon.damage:
                            self.hero.attacking = PLAYER_ATTACK_BY_SPELL_STRING
                        else:
                            self.hero.attacking = PLAYER_ATTACK_BY_WEAPON_STRING
                else:
                    self.hero.attacking = PLAYER_ATTACK_BY_SPELL_STRING
            else:
                if self.hero.spell and self.hero.enough_mana:
                    self.hero.enough_mana = False
                    self.happened +='Hero does not have mana for another ' + self.hero.spell.name + '\n'
                if self.hero.weapon:
                    self.hero.attacking = PLAYER_ATTACK_BY_WEAPON_STRING
                else:
                    self.hero.attacking = 0
                    self.happened += 'Hero has nothing to do.\n'
        elif self.hero.can_cast():
            self.hero.attacking = PLAYER_ATTACK_BY_SPELL_STRING
        else:
            if self.hero.spell and self.hero.enough_mana:
                    self.hero.enough_mana = False
                    self.happened += 'Hero does not have mana for another ' + self.hero.spell.name + '\n'
            self.move_hero()
            self.hero.attacking = None

        if self.hero.attacking:
            if self.hero.attacking == PLAYER_ATTACK_BY_WEAPON_STRING:
                self.happened += 'Hero hits with ' + self.hero.weapon.name
            elif self.hero.attacking == PLAYER_ATTACK_BY_SPELL_STRING:
                self.happened += 'Hero casts a ' + self.hero.spell.name + ', hits enemy'
            else:
                raise ValueError

    def set_enemy_attack(self):
        if not self.distance:
            if self.enemy.can_cast():
                if self.enemy.spell.cast_range >= self.distance:
                    if self.enemy.weapon:
                        if self.enemy.spell.damage >= self.enemy.weapon.damage:
                            self.enemy.attacking = PLAYER_ATTACK_BY_SPELL_STRING
                        else:
                            self.enemy.attacking = PLAYER_ATTACK_BY_WEAPON_STRING
                    else:
                        self.enemy.attacking = PLAYER_ATTACK_BY_SPELL_STRING
                else:
                    self.move_enemy()
                    self.enemy.attacking = None
            else:
                self.enemy.attacking = 0
                if self.enemy.spell and self.enemy.enough_mana:
                        self.enemy.enough_mana = False
                        self.happened += 'Enemy does not have mana for another '  + self.enemy.spell.name + '.\n'
                if self.enemy.weapon:
                    self.enemy.attacking = PLAYER_ATTACK_BY_WEAPON_STRING
                else:
                    self.happened += 'Enemy hits hero'
        elif self.enemy.can_cast():
            if self.enemy.spell.cast_range >= self.distance:
                self.enemy.attacking = PLAYER_ATTACK_BY_SPELL_STRING
            else:
                self.move_enemy()
                self.enemy.attacking = None
        else:
            if self.enemy.spell and self.enemy.enough_mana:
                        self.enemy.enough_mana = False
                        self.happened += 'Enemy does not have mana for another ' + self.enemy.spell.name + '.\n'
            self.move_enemy()
            self.enemy.attacking = None

        if self.enemy.attacking is not None:
            if self.enemy.attacking == PLAYER_ATTACK_BY_WEAPON_STRING:
                self.happened += 'Enemy hits with ' + self.enemy.weapon.name
            elif self.enemy.attacking == PLAYER_ATTACK_BY_SPELL_STRING:
                self.happened += 'Enemy casts a ' + self.enemy.spell.name + ', hits hero'
            else:
                pass # self.enemy.attacking == 0

    def hero_on_turn(self):
        self.set_hero_attack()
        if self.hero.attacking:
            damage = self.hero.attack(by=self.hero.attacking)
            self.enemy.take_damage(damage)
            self.happened += ' for {d} dmg. Enemy health is {h}'.format(d=damage, h=self.enemy.health) + '.\n'

    def enemy_on_turn(self):
        self.set_enemy_attack()
        if self.enemy.attacking is not None:
            if self.enemy.attacking:
                damage = self.enemy.attack(by=self.enemy.attacking)
            else:
                damage = self.enemy.attack()

            self.hero.take_damage(damage)
            self.happened += ' for {d} dmg. Hero health is {h}'.format(d=damage, h=self.hero.health) + '.\n'
        else:
            pass # enemy only moves

    def move_hero(self):
        if self.hero.weapon:
            self.distance -= 1
            self.happened += 'Hero moves one square {d} in\
 order to get to the enemy. This is his move.\n'.format(d=self.direction)
        else:
            self.happened += 'Hero has nothing to do.\n'

    def move_enemy(self):
        self.distance -= 1
        self.happened += 'Enemy moves one square {d} in\
 order to get to the hero. This is his move.\n'.format(d=self.opposite_direction)


if __name__ == '__main__':
    h = Hero(name="Bron", title="Dragonslayer",
             health=100, mana=100, mana_regeneration_rate=2)
    h.learn(Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2))
    # h.equip(Weapon(name="The Axe of Destiny", damage=20))
    e = Enemy()

    # print(Fight(h, e))
    print(Fight(h, e, distance=2, direction='down'))
