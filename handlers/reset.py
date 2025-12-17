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

async def reset(bot: BaseBot, user: User, message: str) -> None:
    try:
        position = Position(x=0, y=0, z=0, facing="FrontLeft")
        await bot.highrise.teleport(user.id, position)
        await bot.highrise.send_whisper(user.id,
                                        "Teleported to default position.")
        await asyncio.sleep(0.5)
    except Exception as e:
        await bot.highrise.send_whisper(
            user.id, f"Error teleporting to default: {e}")
        print(f"Reset teleport error: {e}")
    return