import os
import json

DATA_FOLDER = "data"
USERS_FILE = os.path.join(DATA_FOLDER, "users.json")

# Ensure the data folder exists
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)


class User:
    @classmethod
    def load_users(cls):
        if not os.path.exists(USERS_FILE):
            return {}
        with open(USERS_FILE, "r") as f:
            return json.load(f)

    @classmethod
    def save_users(cls, users):
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)

    @classmethod
    def authenticate(cls, username, password):
        users = cls.load_users()
        return username in users and users[username] == password

    @classmethod
    def register(cls, username, password):
        users = cls.load_users()
        if username in users:
            return False, "Username already exists"
        users[username] = password
        cls.save_users(users)
        return True, "Registration successful"
