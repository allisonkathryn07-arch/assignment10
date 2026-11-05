class Skill:
    def __init__(self, name, cost, cooldown):
        self.name = name
        self.cost = cost
        self.cooldown = cooldown
        self.remaining = 0

    def can_use(self, player):
        return player.mp >= self.cost and self.remaining == 0

    def use(self, player, monster):
        raise NotImplementedError

    def tick(self):
        if self.remaining > 0:
            self.remaining -= 1

class Fireball(Skill):
    def __init__(self):
        super().__init__("Fireball", 15, 2)

    def use(self, player, monster):
        damage = 30 + player.level * 5
        monster.hp -= damage
        player.mp -= self.cost
        self.remaining = self.cooldown
        print(f"Fireball deals {damage} damage!")

class Heal(Skill):
    def __init__(self):
        super().__init__("Heal", 12, 3)

    def use(self, player, monster=None):
        amount = 35 + player.level * 5
        player.hp = min(player.max_hp, player.hp + amount)
        player.mp -= self.cost
        self.remaining = self.cooldown
        print(f"Healed {amount} HP!")

class PowerStrike(Skill):
    def __init__(self):
        super().__init__("Power Strike", 10, 1)

    def use(self, player, monster):
        damage = player.attack * 2
        monster.hp -= damage
        player.mp -= self.cost
        self.remaining = self.cooldown
        print(f"Power Strike deals {damage} damage!")

SKILL_LIBRARY = {
    "Fireball": Fireball,
    "Heal": Heal,
    "Power Strike": PowerStrike }
