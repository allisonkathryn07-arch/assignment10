from tinydb import TinyDB, Query
from pathlib import Path

Path("saves").mkdir(exist_ok=True)
db = TinyDB("saves/accounts.json")
accounts = db.table("accounts")

def create_account(username, password):
    User = Query()
    if accounts.search(User.username == username):
        return False

    accounts.insert({
        "username": username,
        "password": password,
        "progress": None
    })
    return True

def check_login(username, password):
    User = Query()
    result = accounts.search(
        (User.username == username) &
        (User.password == password)
    )
    return result[0] if result else None

def save_progress(username, progress):
    User = Query()
    accounts.update(
        {"progress": progress},
        User.username == username
    )

def load_progress(username):
    User = Query()
    result = accounts.search(User.username == username)
    return result[0]["progress"] if result else None
