class Treasure:
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __repr__(self):
        return str(self.__dict__)


class Spell(Treasure):
    # name, damage, mana_cost, cast_range
    def __str__(self):
        return 'Spell: ' + self.name + ': damage: ' + str(self.damage) + ', cost: ' + str(self.mana_cost) + ', range: ' + str(self.cast_range)

    def set_for_player(self, player):
        player.learn(self)


class Weapon(Treasure):
    # name, damage
    def __str__(self):
        return 'Weapon: ' + self.name + ': damage: ' + str(self.damage)

    def set_for_player(self, player):
        player.equip(self)


class HealthPotion(Treasure):
    # name, healing
    def __str__(self):
        return 'HealthPotion: ' + self.name + ': healing: ' + str(self.healing)

    def set_for_player(self, player):
        player.take_healing(int(self.healing))


class ManaPotion(Treasure):
    def __str__(self):
        return 'ManaPotion: ' + self.name + ': mana: ' + str(self.mana_regen)

    def set_for_player(self, player):
        player.take_mana(int(self.mana_regen))


# treasures = [
# Weapon(name="The Axe of Destiny", damage=20),
# Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2),
# HealthPotion(name="The potion of Undying", healing=50),
# ManaPotion(name="The potion of Unexhausting", mana_regen=50),


