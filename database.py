import json


def load_users():

    with open("users.json", "r", encoding="utf-8") as file:

        users = json.load(file)

    return users

def save_users(users):

    with open("users.json", "w", encoding="utf-8") as file:

        json.dump(
            users,
            file,
            ensure_ascii=False,
            indent=4
        )