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


async def getutils(bot: BaseBot, user: User, message: str):
    result = await find_user(bot, user.username)
    if not result:
        await bot.highrise.send_whisper(user.id,
                                        f"User @{user.username} not found.")
        return

    target_user, position, is_vip, is_mod, is_owner = result

    # Build role summary
    summary = []
    if is_owner:
        summary.append("Owner")
    elif is_mod:
        summary.append("Mod")
    if is_vip:
        summary.append("VIP")

    status_msg = ", ".join(summary) if summary else "None"
    await bot.highrise.send_whisper(user.id, f"Your roles: {status_msg}")
