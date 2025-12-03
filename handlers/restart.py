from highrise import *
from highrise.webapi import *
from highrise.models_webapi import *
from highrise.models import *
from highrise.models import Item
import asyncio
import requests
import random
import re
import os
import sys
from utils import find_user
from tip_manager import load_tips, add_tip, give_vip, remove_vip
from config import BOT_ID, ROOM_ID, BOT_UID, BOT_START_POSITION, VIP_THRESHOLD

tip_lock = asyncio.Lock()

highriseroomID = ROOM_ID


async def restart(bot: BaseBot, user: User, message: str) -> None:
    if message.lower().strip() == "!restart":
        user_info = await find_user(bot, user.username)

        if not user_info:
            await bot.highrise.send_whisper(user_id, "Who even are you bruh 💀")
            return

        _, _, _, _, is_owner = user_info

        if is_owner:
            await bot.highrise.send_whisper(user.id, "Say less. Restarting 🔁")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            await bot.highrise.send_whisper(
                user.id, "Nah fam. Only the room owner can restart me. ✋")
