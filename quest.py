from monster import Goblin, Skeleton, Dragon
from combat import battle

class Quest:
    def __init__(self, name, description, reward_gold, reward_xp):
        self.name = name
        self.description = description
        self.reward_gold = reward_gold
        self.reward_xp = reward_xp
        self.completed = False

    def reward(self, player):
        if self.completed:
            print("This quest is already complete.")
            return

        self.completed = True
        player.gold += self.reward_gold
        player.gain_xp(self.reward_xp)
        print(f"Quest completed: {self.name}!")
        print(
            f"Reward: {self.reward_gold} gold "
            f"and {self.reward_xp} XP."
        )

class MainQuest:
    def __init__(self, stage=0):
        self.stage = stage

    def run(self, player):
        if self.stage == 0:
            print("Stage 1: Defeat the Goblin Scout.")
            if battle(player, Goblin()):
                self.stage = 1

        elif self.stage == 1:
            print("Stage 2: Defeat the Skeleton Guardian.")
            if battle(player, Skeleton()):
                self.stage = 2

        elif self.stage == 2:
            print("Stage 3: Learn Fireball and prepare for the Dragon.")
            if player.learn_skill("Fireball"):
                print("You learned Fireball!")
            self.stage = 3

        elif self.stage == 3:
            print("FINAL STAGE: Defeat the Eldoria Dragon!")
            if battle(player, Dragon(), boss=True):
                self.stage = 4

        elif self.stage == 4:
            print("The Dragon has fallen. Eldoria is saved!")
            return True

        return self.stage == 4

class SideQuests:
    def __init__(self, data=None):
        self.quests = [
            Quest("Wolf Hunt", "Defeat a wolf.", 40, 50),
            Quest("Treasure Hunter", "Collect 3 Health Potions.", 60, 75)
        ]
        if data:
            for quest, completed in zip(self.quests, data):
                quest.completed = completed

    def show(self, player):
        for quest in self.quests:
            status = "Completed" if quest.completed else "Available"
            print(f"{quest.name}: {quest.description} [{status}]")

        choice = input("Complete a side quest? (1/2 or 0): ").strip()

        if choice == "1" and not self.quests[0].completed:
            if battle(player, __import__(
                "monster"
            ).Wolf()):
                self.quests[0].reward(player)

        elif choice == "2" and not self.quests[1].completed:
            if player.inventory.items.get("Health Potion", 0) >= 3:
                player.inventory.remove("Health Potion", 3)
                self.quests[1].reward(player)
            else:
                print("You need 3 Health Potions.")

    def to_list(self):
        return [q.completed for q in self.quests]
