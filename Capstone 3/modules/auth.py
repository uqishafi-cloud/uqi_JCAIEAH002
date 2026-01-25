import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

USER_DB_PATH = os.path.join(project_root, "users.json")

def load_users():
    if not os.path.exists(USER_DB_PATH):
        print("File users.json tidak ditemukan!")
        return {}
    
    with open(USER_DB_PATH, "r") as f:
        return json.load(f)

def authenticate(username, password):
    users = load_users()
    
    if username in users:
        if users[username]["password"] == password:
            return users[username]
            
    return None 