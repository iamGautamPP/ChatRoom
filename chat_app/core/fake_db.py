from models.user_model import UserInDB
from typing import Dict
import json
import os

class DB():
    def __init__(self, filename:str=None):
        if filename is None:
            filename = os.path.join(os.path.dirname(__file__), "db.json")
        self.db_file = filename
        self.users : Dict[str, Dict] = self.load_users()

    def load_users(self) -> Dict[str, Dict]:
        """Load users from the JSON file if it exists, otherwise return an empty dict."""
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return {}
        return {}
    
    def save_users(self):
        """Save the current users dictionary to the JSON file."""
        with open(self.db_file, "w") as file:
            json.dump(self.users, file, indent=4)

    def add_users(self, data:UserInDB):
        data = data.model_dump()
        key = data['username']
        if key in self.users:
            raise ValueError(f"User with username {key} already exists")
        self.users[key] = data
        self.save_users()

    def user_exists(self, username:str):
        return username in self.users



















# dict = {"username":{"username":"Gautam", "email":"abc123@gmail.com", "hashed_password":"cbdcder9yr"}}
# new_user = {"username":"Prasad", "email":"abc123@gmail.com", "hashed_password":"cbdcder9yr"}
# key = new_user['username']
# dict[key]=new_user

# print(dict)