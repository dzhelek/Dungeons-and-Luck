# Antony
class Playable:
    pass


class Hero(Playable):
    pass


class Enemy(Playable):
    damage = random.randrange(100, 200)
    equip_spell(random.choice('spells.txt'))


# Yoan
class Item:
    pass


class Spell(Item):
    pass


class Weapon(Item):
    pass


# to be continued...
class Dungeon:
    pass


class Fight:
    pass


spells.txt:
    -------------------------------------------------
    spell1 = Spell(name='magic of unicorn', damage=20)
    -------------------------------------------------
    spell2 = Spell(name='magic of unicorn', damage=24)
