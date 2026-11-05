from database import create_account, check_login
from colorama import Fore

def authenticate():
    while True:
        print(Fore.CYAN + "\n=== ELDORIA ACCOUNT ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            username = input("Create username: ").strip()
            password = input("Create password: ").strip()

            if not username or not password:
                print(Fore.RED + "Fields cannot be empty.")
            elif len(username) > 20 or len(password) > 64:
                print(Fore.RED + "Username or password too long.")
            elif create_account(username, password):
                print(Fore.GREEN + "Registration successful!")
            else:
                print(Fore.RED + "Username already exists.")

        elif choice == "2":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            account = check_login(username, password)

            if account:
                print(Fore.GREEN + "Login successful!")
                return username
            print(Fore.RED + "Incorrect username or password.")

        elif choice == "3":
            return None
        else:
            print(Fore.RED + "Invalid choice.")
