from highrise import *
from highrise.webapi import *
from highrise.models_webapi import *
from highrise.models import *
from highrise.models import Item
import asyncio
import requests
import random
import re
import json
from utils import find_user
from config import BOT_ID, ROOM_ID, BOT_UID, BOT_START_POSITION, VIP_THRESHOLD

subs_file = "subs.json"


def read_usernames(bot, user, message):
  try:
    with open(subs_file, "r") as f:
      usernames = json.load(f)
      return usernames
  except FileNotFoundError:
    return []


def add_username(bot, user, message):
  try:
    try:
      usernames = read_usernames(subs_file)
    except Exception as e:
      print(f"Error reading usernames: {e}")
      usernames = []  # fallback to empty list if read fails

    if username not in usernames:
      usernames.append(username)
      with open(subs_file, "w") as f:
        json.dump(usernames, f, indent=4)
  except Exception as e:
    print(f"Error adding username: {e}")


def delete_username(bot, user, message):
  try:
    usernames = read_usernames(subs_file)
    if username not in usernames:
      print("Username not Found")
      return
    usernames.remove(username)
    with open(subs_file, "w") as f:
      json.dump(usernames, f, indent=4)
  except Exception as e:
    print(f"Error deleting username: {e}")
