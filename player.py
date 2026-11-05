from inventory import Inventory
from skill import SKILL_LIBRARY

class Player:
    def __init__(self, name, data=None):
        self.name = name

        if data:
            self.hp = data["hp"]
            self.max_hp = data["max_hp"]
            self.mp = data["mp"]
            self.max_mp = data["max_mp"]
            self.level = data["level"]
            self.xp = data["xp"]
            self.gold = data["gold"]
            self.attack = data["attack"]
            self.inventory = Inventory(data["inventory"])
            self.skills = [
                SKILL_LIBRARY[s]() for s in data["skills"]
            ]
        else:
            self.level = 1
            self.xp = 0
            self.gold = 50
            self.max_hp = 100
            self.hp = 100
            self.max_mp = 50
            self.mp = 50
            self.attack = 15
            self.inventory = Inventory({
                "Health Potion": 2
            })
            self.skills = [SKILL_LIBRARY["Power Strike"]()]

    def gain_xp(self, amount):
        self.xp += amount
        print(f"Gained {amount} XP!")

        while self.xp >= self.level * 100:
            self.xp -= self.level * 100
            self.level += 1
            self.max_hp += 20
            self.max_mp += 10
            self.attack += 5
            self.hp = self.max_hp
            self.mp = self.max_mp
            print(f"LEVEL UP! You are now level {self.level}!")

    def learn_skill(self, name):
        if name not in SKILL_LIBRARY:
            return False
        if any(s.name == name for s in self.skills):
            return False
        self.skills.append(SKILL_LIBRARY[name]())
        return True

    def show_status(self):
        print("\n=== CHARACTER STATUS ===")
        print(f"Name: {self.name}")
        print(f"Level: {self.level}")
        print(f"XP: {self.xp}/{self.level * 100}")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"MP: {self.mp}/{self.max_mp}")
        print(f"Attack: {self.attack}")
        print(f"Gold: {self.gold}")
        print("Skills:", ", ".join(s.name for s in self.skills))

    def to_dict(self):
        return {
            "hp": self.hp,
            "max_hp": self.max_hp,
            "mp": self.mp,
            "max_mp": self.max_mp,
            "level": self.level,
            "xp": self.xp,
            "gold": self.gold,
            "attack": self.attack,
            "inventory": self.inventory.items,
            "skills": [s.name for s in self.skills] }
