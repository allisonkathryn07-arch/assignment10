from item import ITEMS

def visit_shop(player):
    while True:
        print("\n=== THORIN'S SHOP ===")

        for i, item in enumerate(ITEMS.values(), 1):
            print(f"{i}. {item.name} - {item.price} gold")

        print("0. Leave shop")
        print(f"Your gold: {player.gold}")

        choice = input("Buy item: ").strip()

        if choice == "0":
            return

        try:
            index = int(choice) - 1
            item_list = list(ITEMS.values())

            if index < 0 or index >= len(item_list):
                raise ValueError

            item = item_list[index]

            if player.gold < item.price:
                print("Not enough gold!")
                continue

            if item.item_type == "weapon" and player.inventory.items.get(item.name, 0):
                print("You already own this weapon.")
                continue

            player.gold -= item.price
            player.inventory.add(item.name)
            print(f"Purchased {item.name}!")

        except ValueError:
            print("Please enter a valid number.")
