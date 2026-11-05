from tinydb import TinyDB, Query
from colorama import init, Fore
import random

init(autoreset=True)

db = TinyDB("save.json")
User = Query()

# =========================
# SKILLS
# =========================

class Skill:
    def __init__(self, name, cooldown):
        self.name = name
        self.cooldown = cooldown

class Fireball(Skill):
    def __init__(self):
        super().__init__("Fireball", 2)

    def use(self, monster):
        dmg = 25
        monster.hp -= dmg
        print(Fore.RED + f"Fireball deals {dmg} damage!")

class Heal(Skill):
    def __init__(self):
        super().__init__("Heal", 3)

    def use(self, player):
        heal = 20
        player.hp = min(player.max_hp, player.hp + heal)
        print(Fore.GREEN + f"Healed {heal} HP!")

class PowerStrike(Skill):
    def __init__(self):
        super().__init__("Power Strike", 1)

    def use(self, monster):
        dmg = 35
        monster.hp -= dmg
        print(Fore.RED + f"Power Strike deals {dmg} damage!")

# =========================
# MONSTERS
# =========================

class Monster:
    def __init__(self, name, hp, attack, gold, exp):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.gold = gold
        self.exp = exp

class Goblin(Monster):
    def __init__(self):
        super().__init__("Goblin", 30, 5, 15, 25)

class Wolf(Monster):
    def __init__(self):
        super().__init__("Wolf", 40, 7, 20, 35)

class Skeleton(Monster):
    def __init__(self):
        super().__init__("Skeleton", 60, 10, 35, 50)

class Orc(Monster):
    def __init__(self):
        super().__init__("Orc", 90, 14, 50, 75)

class ShadowLord(Monster):
    def __init__(self):
        super().__init__("Shadow Lord", 250, 25, 300, 500)

# =========================
# PLAYER
# =========================

class Player:
    def __init__(self, username):
        self.username = username
        self.level = 1
        self.exp = 0
        self.hp = 100
        self.max_hp = 100
        self.gold = 50
        self.inventory = ["Potion"]
        self.skills = ["Fireball"]
        self.location = "Town"
        self.quest_step = 0
        self.side_quests = {
            "herbs": False,
            "wolves": False
        }

    def gain_exp(self, amount):
        self.exp += amount

        while self.exp >= self.level * 100:
            self.exp -= self.level * 100
            self.level += 1
            self.max_hp += 20
            self.hp = self.max_hp

            print(Fore.GREEN + f"LEVEL UP! Level {self.level}")

# =========================
# SAVE / LOAD
# =========================

def save_player(player):

    db.update({
        "level": player.level,
        "exp": player.exp,
        "hp": player.hp,
        "max_hp": player.max_hp,
        "gold": player.gold,
        "inventory": player.inventory,
        "skills": player.skills,
        "location": player.location,
        "quest_step": player.quest_step,
        "side_quests": player.side_quests
    }, User.username == player.username)

    print(Fore.CYAN + "Game Saved!")

def load_player(username):

    data = db.search(User.username == username)[0]

    player = Player(username)

    player.level = data["level"]
    player.exp = data["exp"]
    player.hp = data["hp"]
    player.max_hp = data["max_hp"]
    player.gold = data["gold"]
    player.inventory = data["inventory"]
    player.skills = data["skills"]
    player.location = data["location"]
    player.quest_step = data["quest_step"]
    player.side_quests = data["side_quests"]

    return player

# =========================
# LOGIN
# =========================

def register():

    username = input("Username: ")
    password = input("Password: ")

    if db.search(User.username == username):
        print("Account exists!")
        return None

    db.insert({
        "username": username,
        "password": password,
        "level": 1,
        "exp": 0,
        "hp": 100,
        "max_hp": 100,
        "gold": 50,
        "inventory": ["Potion"],
        "skills": ["Fireball"],
        "location": "Town",
        "quest_step": 0,
        "side_quests": {
            "herbs": False,
            "wolves": False
        }
    })

    print("Account Created!")

def login():

    username = input("Username: ")
    password = input("Password: ")

    result = db.search(
        (User.username == username)
        &
        (User.password == password)
    )

    if result:
        print("Login Successful")
        return load_player(username)

    print("Incorrect Login")
    return None

# =========================
# NPCS
# =========================

npcs = {
    "Village Elder": "Please recover the relics and save our kingdom.",
    "Blacksmith": "I can forge legendary weapons.",
    "Merchant": "Interested in some goods?",
    "Hunter": "Wolves are everywhere lately.",
    "Wizard": "Magic is the key to victory."
}

def talk_npcs():

    print("\nNPCs:")

    for npc in npcs:
        print("-", npc)

    npc = input("Who? ")

    if npc in npcs:
        print(Fore.YELLOW + npcs[npc])

# =========================
# CHARACTER
# =========================

def show_character(player):

    print("\n====== CHARACTER ======")
    print("Name:", player.username)
    print("Level:", player.level)
    print("HP:", player.hp, "/", player.max_hp)
    print("XP:", player.exp)
    print("Gold:", player.gold)
    print("Skills:", player.skills)
    print("Inventory:", player.inventory)
    print("Quest Step:", player.quest_step)

# =========================
# INVENTORY
# =========================

def inventory_menu(player):

    print("\nInventory")

    for i,item in enumerate(player.inventory):
        print(i+1, item)

    choice = input("Use Potion? (y/n): ")

    if choice.lower() == "y":

        if "Potion" in player.inventory:

            player.inventory.remove("Potion")

            player.hp = min(player.max_hp, player.hp + 30)

            print(Fore.GREEN + "Potion Used")

# =========================
# SHOP
# =========================

def shop(player):

    items = {
        "Potion":20,
        "Super Potion":50
    }

    print("\nSHOP")

    for item,price in items.items():
        print(item, "-", price)

    buy = input("Buy: ")

    if buy in items:

        if player.gold >= items[buy]:

            player.gold -= items[buy]
            player.inventory.append(buy)

            print(Fore.GREEN + "Purchased!")

        else:
            print("Not enough gold")

# =========================
# COMBAT
# =========================

def choose_monster():

    monsters = [
        Goblin(),
        Wolf(),
        Skeleton(),
        Orc()
    ]

    return random.choice(monsters)

def combat(player, monster):

    print(Fore.RED + f"\nA {monster.name} appears!")

    while monster.hp > 0 and player.hp > 0:

        print("\n1 Attack")
        print("2 Skill")
        print("3 Run")

        choice = input("> ")

        if choice == "1":

            dmg = random.randint(8,15)
            monster.hp -= dmg

            print(f"You deal {dmg}")

        elif choice == "2":

            print(player.skills)

            s = input("Skill: ")

            if s == "Fireball":
                Fireball().use(monster)

            elif s == "Heal":
                Heal().use(player)

            elif s == "Power Strike":
                PowerStrike().use(monster)

        elif choice == "3":
            return

        if monster.hp > 0:

            player.hp -= monster.attack

            print(
                Fore.RED +
                f"{monster.name} deals {monster.attack}"
            )

        print(
            f"Monster HP: {max(monster.hp,0)}"
        )

    if player.hp <= 0:

        print(Fore.RED + "GAME OVER")
        exit()

    print(Fore.GREEN + "Victory!")

    player.gold += monster.gold
    player.gain_exp(monster.exp)

    print(Fore.YELLOW + f"+{monster.gold} Gold")
    print(Fore.CYAN + f"+{monster.exp} EXP")

    if random.randint(1,100) <= 25:
        player.inventory.append("Potion")
        print(Fore.GREEN + "Potion Dropped!")

# =========================
# QUESTS
# =========================

def main_quest(player):

    if player.quest_step == 0:

        print(
            Fore.CYAN +
            "Quest 1: Speak with Village Elder"
        )

        player.quest_step = 1

    elif player.quest_step == 1:

        print(
            Fore.CYAN +
            "Quest 2: Defeat Goblins"
        )

        player.quest_step = 2

    elif player.quest_step == 2:

        print(
            Fore.CYAN +
            "Quest 3: Retrieve Relic"
        )

        player.quest_step = 3

    elif player.quest_step == 3:

        print(
            Fore.CYAN +
            "Quest 4: Defeat Orc Chief"
        )

        player.quest_step = 4

    elif player.quest_step == 4:

        print(
            Fore.CYAN +
            "Final Quest: Defeat Shadow Lord"
        )

        boss = ShadowLord()

        combat(player, boss)

        print(
            Fore.GREEN +
            "YOU SAVED THE KINGDOM!"
        )

        exit()

# =========================
# SIDE QUESTS
# =========================

def side_quests(player):

    print("\n1 Herb Gathering")
    print("2 Wolf Hunt")

    choice = input("> ")

    if choice == "1":

        if not player.side_quests["herbs"]:

            player.gold += 50
            player.side_quests["herbs"] = True

            print("Reward: 50 Gold")

    elif choice == "2":

        if not player.side_quests["wolves"]:

            player.gain_exp(100)
            player.side_quests["wolves"] = True

            print("Reward: 100 EXP")

# =========================
# MAPS
# =========================

def show_map(location):

    if location == "Town":

        print("""
##########
#P    N  #
# ##     #
#   S    #
##########
""")

    else:

        print("""
############
#P     M   #
# ###      #
#     ###  #
#   M      #
############
""")

# =========================
# STORY
# =========================

def intro():

    print(Fore.MAGENTA)
    print("===================================")
    print("      KINGDOM OF ELDORIA")
    print("=================")

    print("""
The Shadow Lord has stolen
the Ancient Relics.

The kingdom is falling into darkness.

Only you can stop him.
""")

# =========================
# GAME LOOP
# =========================

def game(player):

    intro()

    while True:

        print("\n===== MENU =====")
        print("1 Character")
        print("2 Map")
        print("3 Explore")
        print("4 NPC")
        print("5 Shop")
        print("6 Inventory")
        print("7 Main Quest")
        print("8 Side Quest")
        print("9 Save")
        print("10 Exit")

        choice = input("> ")

        if choice == "1":
            show_character(player)

        elif choice == "2":
            show_map(player.location)

        elif choice == "3":
            combat(player, choose_monster())

        elif choice == "4":
            talk_npcs()

        elif choice == "5":
            shop(player)

        elif choice == "6":
            inventory_menu(player)

        elif choice == "7":
            main_quest(player)

        elif choice == "8":
            side_quests(player)

        elif choice == "9":
            save_player(player)

        elif choice == "10":
            save_player(player)
            break

# =========================
# START
# =========================

while True:

    print("\n1 Register")
    print("2 Login")
    print("3 Quit")

    start = input("> ")

    if start == "1":
        register()

    elif start == "2":

        player = login()

        if player:
            game(player)

    elif start == "3":
        break