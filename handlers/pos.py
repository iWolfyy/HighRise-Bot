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


async def pos(bot: BaseBot, user: User, message: str) -> None:
    try:
        parts = message.split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(user.id, "Usage: !pos <@username>")
            return

        target_username = parts[1][1:].lower()
        match = await find_user(bot, target_username)
        if not match:
            await bot.highrise.send_whisper(
                user.id, f"User @{target_username} not found.")
            return

        target_user, position, _, _, _ = match
        await bot.highrise.send_whisper(
            user.id,
            f"@{target_username}'s position:\nX={position.x}, Y={position.y}, Z={position.z}"
        )
        await asyncio.sleep(0.5)

    except Exception as e:
        await bot.highrise.send_whisper(
            user.id, f"Error getting position for @{target_username}: {e}")
        print(f"Pos error: {e}")
