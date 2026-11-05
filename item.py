class Item:
    def __init__(self, name, description, price, item_type, power):
        self.name = name
        self.description = description
        self.price = price
        self.item_type = item_type
        self.power = power

POTION = Item(
    "Health Potion", "Restores 40 HP", 20, "heal", 40 )

SUPER_POTION = Item(
    "Super Potion", "Restores 100 HP", 50, "heal", 100 )

ETHER = Item(
    "Ether", "Restores 30 MP", 25, "mana", 30 )

IRON_SWORD = Item(
    "Iron Sword", "A stronger weapon", 75, "weapon", 5 )

ITEMS = {
    item.name: item for item in
    [POTION, SUPER_POTION, ETHER, IRON_SWORD] }
