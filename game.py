from colorama import Fore, Style, init
from player import Player
from database import load_progress, save_progress
from quest import MainQuest, SideQuests
from npc import meet_npc
from shop import visit_shop
from game_map import FOREST, DUNGEON
from monster import random_monster
from combat import battle
import random

init(autoreset=True)

class Game:
    def __init__(self, username):
        self.username = username
        data = load_progress(username)

        if data:
            self.player = Player(username, data["player"])
            self.main_quest = MainQuest(data["main_stage"])
            self.side_quests = SideQuests(data["side_quests"])

            map_data = data.get("map", {})
            self.current_map = (
                DUNGEON if map_data.get("name") == "Ancient Dungeon"
                else FOREST
            )
            self.current_map.player_x = map_data.get("x", 1)
            self.current_map.player_y = map_data.get("y", 1)

        else:
            self.player = Player(username)
            self.main_quest = MainQuest()
            self.side_quests = SideQuests()
            self.current_map = FOREST

    def save(self):
        data = {
            "player": self.player.to_dict(),
            "main_stage": self.main_quest.stage,
            "side_quests": self.side_quests.to_list(),
            "map": {
                "name": self.current_map.name,
                "x": self.current_map.player_x,
                "y": self.current_map.player_y
            }
        }
        save_progress(self.username, data)

    def intro(self):
        print(Fore.CYAN + """
==========================================
       LEGENDS OF ELDORIA
          THE SHATTERED CROWN
==========================================

A thousand years ago, Eldoria was protected
by a magical crown.

Now the crown has shattered, and an ancient
Dragon has awakened.

The kingdom is falling into darkness.

You are the last hope of Eldoria.

Your adventure begins now...
==========================================
""")

        input("Press ENTER to begin...")

    def travel(self):
        print("\n1. Whispering Forest")
        print("2. Ancient Dungeon")
        choice = input("Travel to: ").strip()

        if choice == "1":
            self.current_map = FOREST
            self.current_map.player_x = 1
            self.current_map.player_y = 1
        elif choice == "2":
            self.current_map = DUNGEON
            self.current_map.player_x = 1
            self.current_map.player_y = 1
        else:
            print("Invalid destination.")

    def explore(self):
        while True:
            self.current_map.display()
            print("\nW/A/S/D = Move | Q = Return")
            direction = input("Direction: ").lower().strip()

            if direction == "q":
                break

            reached_exit = self.current_map.move(direction)

            if reached_exit:
                print("You discovered a hidden treasure!")
                self.player.gold += 30
                self.player.gain_xp(20)
                break

            # Random encounters while exploring.
            if direction in ("w", "a", "s", "d"):
                if random.random() < 0.25:
                    battle(self.player, random_monster())

                if self.player.hp <= 0:
                    break

            self.save()

    def npc_menu(self):
        print("\n=== CHARACTERS ===")
        names = [
            "Elder Rowan",
            "Mira the Healer",
            "Thorin the Blacksmith",
            "Luna the Mage",
            "Captain Aldric"
        ]

        for i, name in enumerate(names, 1):
            print(f"{i}. {name}")

        print("0. Return")

        choice = input("Talk to: ").strip()

        try:
            number = int(choice)
            if number == 0:
                return
            meet_npc(number, self.player)
            self.save()
        except ValueError:
            print("Invalid selection.")

    def menu(self):
        while True:
            print(Fore.CYAN + """
========== ELDORIA ==========
1. View character status
2. View inventory
3. Explore map
4. Travel
5. Talk to NPCs
6. Main quest
7. Side quests
8. Visit shop
9. Save game
0. Save and exit
=============================
""")

            choice = input("Choose an action: ").strip()

            if choice == "1":
                self.player.show_status()

            elif choice == "2":
                self.player.inventory.show()
                name = input("Use an item (or ENTER to cancel): ").strip()
                if name:
                    self.player.inventory.use(name, self.player)

            elif choice == "3":
                self.explore()

            elif choice == "4":
                self.travel()

            elif choice == "5":
                self.npc_menu()

            elif choice == "6":
                completed = self.main_quest.run(self.player)
                self.save()

                if completed:
                    print(Fore.GREEN + """
****************************************
       CONGRATULATIONS, HERO!
       ELDORIA HAS BEEN SAVED!
****************************************
""")
                    self.save()
                    break

            elif choice == "7":
                self.side_quests.show(self.player)
                self.save()

            elif choice == "8":
                visit_shop(self.player)
                self.save()

            elif choice == "9":
                self.save()
                print("Game saved!")

            elif choice == "0":
                self.save()
                print("Progress saved. Goodbye!")
                break

            else:
                print(Fore.RED + "Invalid selection.")

    def start(self):
        if load_progress(self.username) is None:
            self.intro()

        self.menu()
