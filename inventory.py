from item import ITEMS

class Inventory:
    def __init__(self, data=None):
        self.items = data if data else {}

    def add(self, name, amount=1):
        if name not in ITEMS:
            return False
        self.items[name] = self.items.get(name, 0) + amount
        return True

    def remove(self, name, amount=1):
        if self.items.get(name, 0) < amount:
            return False

        self.items[name] -= amount

        if self.items[name] <= 0:
            del self.items[name]

        return True

    def show(self):
        print("\n=== INVENTORY ===")

        if not self.items:
            print("Your inventory is empty.")
            return

        for name, quantity in self.items.items():
            print(f"{name} x{quantity}")

    def use(self, name, player):
        if name not in self.items:
            print("You don't have that item.")
            return

        item = ITEMS[name]

        if item.item_type == "heal":
            if player.hp >= player.max_hp:
                print("Your HP is already full.")
                return
            player.hp = min(player.max_hp, player.hp + item.power)

        elif item.item_type == "mana":
            player.mp = min(player.max_mp, player.mp + item.power)

        elif item.item_type == "weapon":
            player.attack += item.power

        else:
            return

        self.remove(name)
        print(f"You used {name}!")
