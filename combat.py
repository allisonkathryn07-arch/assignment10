from colorama import Fore
import random

def battle(player, monster, boss=False):
    print(Fore.RED + f"\nA {monster.name} appears!")

    while player.hp > 0 and monster.is_alive():
        print(
            f"\nYour HP: {player.hp}/{player.max_hp} | "
            f"MP: {player.mp}/{player.max_mp}"
        )
        print(f"{monster.name} HP: {monster.hp}/{monster.max_hp}")

        print("\n1. Attack")
        print("2. Skills")
        print("3. Use item")
        print("4. Run")

        choice = input("Action: ").strip()

        if choice == "1":
            damage = player.attack + random.randint(0, 5)
            monster.hp -= damage
            print(Fore.GREEN + f"You deal {damage} damage!")

        elif choice == "2":
            for i, skill in enumerate(player.skills, 1):
                print(
                    f"{i}. {skill.name} "
                    f"(MP {skill.cost}, cooldown {skill.remaining})"
                )

            try:
                index = int(input("Choose skill: ")) - 1
                if index < 0 or index >= len(player.skills):
                    raise ValueError

                skill = player.skills[index]

                if not skill.can_use(player):
                    print("Not enough MP or skill is cooling down.")
                    continue

                skill.use(player, monster)

            except ValueError:
                print("Invalid skill selection.")
                continue

        elif choice == "3":
            player.inventory.show()
            name = input("Item name (or blank to cancel): ").strip()

            if name:
                player.inventory.use(name, player)
            continue

        elif choice == "4":
            if boss:
                print("You cannot escape the final battle!")
                continue
            print("You escaped!")
            return False

        else:
            print("Invalid action.")
            continue

        if not monster.is_alive():
            break

        # The monster gets a turn.
        damage = max(1, monster.attack - random.randint(0, 3))
        player.hp = max(0, player.hp - damage)
        print(Fore.RED + f"{monster.name} hits you for {damage}!")

        # Cooldowns decrease after each enemy turn.
        for skill in player.skills:
            skill.tick()

    if player.hp <= 0:
        print(Fore.RED + "You were defeated!")
        return False

    print(Fore.GREEN + f"\nYou defeated {monster.name}!")
    player.gold += monster.gold
    player.gain_xp(monster.xp)

    drop = monster.loot()
    if drop:
        player.inventory.add(drop)
        print(f"The monster dropped {drop}!")

    return True
