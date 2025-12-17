from highrise import *
from highrise.webapi import *
from highrise.models_webapi import *
from highrise.models import *
from highrise.models import Item
import asyncio
import requests
import random
import re
from tip_manager import load_tips, add_tip, give_vip, remove_vip
from config import BOT_ID, ROOM_ID, BOT_UID, BOT_START_POSITION, VIP_THRESHOLD


async def find_user(
    bot: BaseBot,
    username: str) -> tuple[User, Position, bool, bool, bool] | None:
  """
  Returns a tuple of:
  - user: User object
  - position: Position object
  - is_vip: bool
  - is_mod: bool
  - is_owner: bool
  Returns None if user is not found.
  """
  try:
    # Step 1: Find user from room
    users = await bot.highrise.get_room_users()
    match = next(((u, pos) for u, pos in users.content
                  if u.username.lower() == username.lower()), None)
    if not match:
      return None

    user, position = match

    # Step 2: VIP check
    tips_data = load_tips()
    user_data = tips_data.get(username.lower(), {"amount": 0, "vip": False})
    is_vip = user_data["vip"]

    # Step 3: Owner & Mod check
    try:
      room_data: SessionMetadata = await bot.webapi.get_room(ROOM_ID)
      owner_id = room_data.room.owner_id
      is_owner = user.id == owner_id or user.username.lower() == "mr_wolfy"


      priv = await bot.highrise.get_room_privilege(user.id)
      is_mod = priv.moderator
    except Exception as e:
      print(f"Privilege check failed: {e}")
      is_owner = False
      is_mod = False

    return user, position, is_vip, is_mod, is_owner

  except Exception as e:
    print(f"Error in find_user: {e}")
    return None