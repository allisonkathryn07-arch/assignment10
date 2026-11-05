import random

class Monster:
    def __init__(self, name, hp, attack, xp, gold, drop=None):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.xp = xp
        self.gold = gold
        self.drop = drop

    def is_alive(self):
        return self.hp > 0

    def loot(self):
        result = random.randint(1, 100)
        return self.drop if self.drop and result <= 50 else None

class Goblin(Monster):
    def __init__(self):
        super().__init__("Goblin", 40, 8, 25, 15, "Health Potion")

class Wolf(Monster):
    def __init__(self):
        super().__init__("Wolf", 55, 12, 35, 20, "Health Potion")

class Skeleton(Monster):
    def __init__(self):
        super().__init__("Skeleton", 70, 15, 45, 25, "Ether")

class DarkKnight(Monster):
    def __init__(self):
        super().__init__("Dark Knight", 110, 20, 70, 40, "Super Potion")

class Dragon(Monster):
    def __init__(self):
        super().__init__("Eldoria Dragon", 300, 25, 300, 250, None)

def random_monster():
    monster_class = random.choice([
        Goblin, Wolf, Skeleton, DarkKnight ])
    return monster_class()
