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


async def ban(bot: BaseBot, user: User, message: str) -> None:
    try:
        # Check if command user has privileges
        match = await find_user(bot, user.username)
        if not match:
            await bot.highrise.send_whisper(
                user.id, f"User @{user.username} not found.")
            return
        _, _, _, is_mod, is_owner = match

        if not (is_mod or is_owner):
            await bot.highrise.send_whisper(
                user.id, "You need moderator privileges to use !ban.")
            return

        # Parse target
        parts = message.split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(user.id, "Usage: !ban <@username>")
            return
        target_username = parts[1][1:].lower()

        target_match = await find_user(bot, target_username)
        if not target_match:
            await bot.highrise.send_whisper(
                user.id, f"User @{target_username} not found.")
            return

        target_user, *_ = target_match

        try:
            await bot.highrise.moderate_room(target_user.id, "ban", None)
            await bot.highrise.send_whisper(user.id,
                                            f"Banned @{target_username}.")
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error banning @{target_username}: {e}")
            print(f"Ban error: {e}")

    except Exception as e:
        await bot.highrise.send_whisper(
            user.id, f"Unexpected error processing !ban: {e}")
        print(f"Unexpected ban command error: {e}")
