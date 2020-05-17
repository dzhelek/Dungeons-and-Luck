from choose import choose_random_treasure_from_file
from constants import (PLAYER_ATTACK_BY_SPELL_STRING,
                       PLAYER_ATTACK_BY_WEAPON_STRING)
from fight import Fight
from enemy import Enemy


class Dungeon:
    def __init__(self, file):
        self.map = self.to_string(file=file)
        self.validate_map()
        self.treasures_file = file.replace('.txt', '_treasures.txt')
        self.checkpoint = 0

    @classmethod
    def from_string(cls, string):
        with open("test.txt", 'w') as f:
            f.write(string)
        return cls(file="test.txt")

    def to_string(self, file=None, list=None):
        if file:
            with open(file, 'r') as f:
                return f.read()
        elif list:
            return "\n".join(["".join(lst) for lst in list])
        else:
            raise ValueError

    def validate_map(self):
        assert 'S' in self.map, "No starting point"

        gates = 0
        for symbol in self.map:
            if symbol == "G":
                gates += 1
        assert gates == 1, "Number of gates != 1"

        self.to_list()
        lens = [len(lst) for lst in self.list_map]
        assert all(lens[0] == length for length in lens)

    def print_map(self):
        print(self.map)

    def spawn(self, hero):
        if 'H' in self.map:
            return False
        if 'S' in self.map:
            self.hero = hero
            self. map = self.map.replace('S', 'H', 1)
            return True
        else:
            return False

    def move_hero(self, direction):
        current_x, current_y = self.get_current_position()
        new_x, new_y = current_x, current_y

        if direction == 'right':
            new_x = current_x + 1
        elif direction == 'left':
            new_x = current_x - 1
            if new_x < 0:
                return False
        elif direction == 'up':
            new_y = current_y - 1
            if new_y < 0:
                return False
        elif direction == 'down':
            new_y = current_y + 1
        else:
            return False

        try:
            if self.list_map[new_y][new_x] == '#':
                return False

            elif self.list_map[new_y][new_x] == '.':
                self.update_hero_position(current_x, current_y, new_x, new_y)
                self.hero.take_mana(self.hero.mana_regeneration_rate)

                return True

            elif self.list_map[new_y][new_x] == 'T':
                treasure = self.pick_treasure()
                self.update_hero_position(current_x, current_y, new_x, new_y)

                return treasure

            elif self.list_map[new_y][new_x] == 'E':
                fight = Fight(self.hero, Enemy())
                if self.hero.is_alive():
                    self.update_hero_position(current_x, current_y,
                                              new_x, new_y)
                elif self.checkpoint:
                    self.update_hero_position(current_x,
                                              current_y,
                                              self.checkpoint[1],
                                              self.checkpoint[0])
                    self.checkpoint = 0
                    self.hero.health = 100

                return fight

            elif self.list_map[new_y][new_x] == 'C':
                self.checkpoint = (new_y, new_x)
                self.update_hero_position(current_x, current_y, new_x, new_y)

                return True

            else:
                return self.list_map[new_y][new_x]
        except IndexError:
            return False

    def update_hero_position(self, current_x, current_y, new_x, new_y):
        self.list_map[current_y][current_x] = '.'
        self.list_map[new_y][new_x] = 'H'
        self.map = self.to_string(list=self.list_map)

    def to_list(self):
        self.list_map = [[]]
        i = 0
        for symbol in self.map:
            if symbol == '\n':
                self.list_map.append([])
                i += 1
            else:
                self.list_map[i].append(symbol)

    def pick_treasure(self, string=None):
        treasure = choose_random_treasure_from_file(self.treasures_file)
        self.hero.set_treasure(treasure)

        return treasure

    def get_current_position(self):
        self.to_list()
        position = self.map.replace('\n', '').index('H')
        x = position % len(self.list_map[0])
        y = position // len(self.list_map[0])

        return (x, y)

    def enemy_in_casting_range(self, direction):
        if 'E' in self.map:
            x, y = self.get_current_position()

            self.distance = 0
            for i in range(self.hero.spell.cast_range):
                self.distance += 1
                if direction == 'right':
                    x += 1
                elif direction == 'left':
                    x -= 1
                elif direction == 'up':
                    y -= 1
                elif direction == 'down':
                    y += 1
                else:
                    return False
                if x < 0:
                    return False
                if y < 0:
                    return False
                try:
                    if self.list_map[y][x] != '.':
                        break
                except IndexError:
                    return False
            if self.list_map[y][x] == 'E':
                return (x, y)
            else:
                return False
        else:
            return False

    def hero_attack(self, by, direction):
        if by == PLAYER_ATTACK_BY_SPELL_STRING:
            try:
                enemy_x, enemy_y = self.enemy_in_casting_range(direction)
            except TypeError:
                return "Nothing in casting range {x}".format(x=self.hero.spell.cast_range)
            else:
                fight = Fight(self.hero, Enemy(),
                              distance=self.distance, direction=direction)
                current_x, current_y = self.get_current_position()
                if self.hero.is_alive():
                    self.update_hero_position(current_x, current_y,
                                              enemy_x, enemy_y)
                elif self.checkpoint:
                    self.update_hero_position(current_x,
                                              current_y,
                                              self.checkpoint[1],
                                              self.checkpoint[0])
                    self.checkpoint = 0
                    self.hero.health = 100

                return fight
        elif by == PLAYER_ATTACK_BY_WEAPON_STRING:
            return "Weapon range is 0!"
        else:
            return "Cannot attack by {x}".format(x=by)
