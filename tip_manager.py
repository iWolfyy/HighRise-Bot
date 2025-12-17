import json
import os
from config import VIP_THRESHOLD

TIPS_FILE = "tips.json"

def load_tips():
    if not os.path.exists(TIPS_FILE):
        return {}
    with open(TIPS_FILE, "r") as file:
        return json.load(file)

def save_tips(data):
    with open(TIPS_FILE, "w") as file:
        json.dump(data, file, indent=4)

def add_tip(username, amount):
    data = load_tips()
    username = username.lower()
    if username not in data:
        data[username] = {"amount": 0, "vip": False}
    data[username]["amount"] += amount
    data[username]["vip"] = data[username]["amount"] >= VIP_THRESHOLD
    save_tips(data)

def give_vip(username):
    data = load_tips()
    username = username.lower()
    if username not in data:
        data[username] = {"amount": 0, "vip": True}
    else:
        data[username]["vip"] = True
    save_tips(data)

def remove_vip(username):
    data = load_tips()
    username = username.lower()
    if username in data:
        data[username]["vip"] = False
        save_tips(data)
        return True
    return False