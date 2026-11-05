from colorama import Fore

class NPC:
    def __init__(self, name, dialogue):
        self.name = name
        self.dialogue = dialogue

    def talk(self):
        print(Fore.YELLOW + f"\n{self.name}:")
        print(f'"{self.dialogue}"')


def meet_npc(number, player):
    npcs = [
        NPC("Elder Rowan",
            "The Dragon has awakened. You must find the strength to stop it."),
        NPC("Mira the Healer",
            "Even the strongest hero needs healing. Take care of yourself."),
        NPC("Blacksmith Thorin",
            "A good sword is worth more than a thousand brave words."),
        NPC("Luna the Mage",
            "Magic is not about power. It is about knowing when to use it."),
        NPC("Captain Aldric",
            "The eastern forest is dangerous. Never underestimate its monsters.")
    ]

    if 1 <= number <= len(npcs):
        npcs[number - 1].talk()

        if number == 1:
            print("Your main quest begins!")
        elif number == 2:
            player.hp = player.max_hp
            player.mp = player.max_mp
            print("Mira restored your HP and MP!")
        elif number == 4:
            if player.learn_skill("Heal"):
                print("You learned Heal!")
            else:
                print("You already know Heal.")
