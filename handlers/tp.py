from highrise import *
from highrise.webapi import *
from highrise.models_webapi import *
from highrise.models import *
from highrise.models import Item
import asyncio
import requests
import random
import re
from utils import find_user
from tip_manager import load_tips, add_tip, give_vip, remove_vip
from config import BOT_ID, ROOM_ID, BOT_UID, BOT_START_POSITION, VIP_THRESHOLD

tip_lock = asyncio.Lock()

highriseroomID = ROOM_ID


async def tp(bot: BaseBot, user: User, message: str) -> None:
    try:
        parts = message.split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(user.id, "Usage: !tp <@username>")
            return
        target_username = parts[1][1:].lower()
        match = await find_user(bot, target_username)
        if not match:
            await bot.highrise.send_whisper(
                user.id, f"User @{target_username} not found.")
            return

        # Unpack all 5 values from find_user
        target_user, target_position, _, _, _ = match

        if not target_position:
            await bot.highrise.send_whisper(
                user.id, f"Could not retrieve @{target_username}'s position.")
            return
        exact_position = Position(x=target_position.x,
                                  y=target_position.y,
                                  z=target_position.z,
                                  facing=target_position.facing or "FrontLeft")
        await bot.highrise.teleport(user.id, exact_position)
        await bot.highrise.send_whisper(user.id,
                                        f"Teleported to @{target_username}.")
        await asyncio.sleep(0.5)
    except Exception as e:
        await bot.highrise.send_whisper(user.id, f"Error processing !tp: {e}")
        print(f"Teleport command error: {e}")
    return
