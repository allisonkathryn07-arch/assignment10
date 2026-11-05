from auth import authenticate
from game import Game
from colorama import Fore, init

init(autoreset=True)

def main():
    print(Fore.YELLOW + """
====================================
       WELCOME TO ELDORIA
====================================
""")

    username = authenticate()

    if username is None:
        print("Thanks for playing!")
        return

    game = Game(username)
    game.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted. Log in again to continue.")