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


async def feedback(bot: BaseBot, user: User, message: str) -> None:
    """Sends feedback info to the user via whisper."""
    try:
        msg = "✨ Bot crafted by @Mr_Wolfy 📩 DM @Mr_Wolfy to make / design your own bot"
        print(
            f"Preparing feedback message for {user.username}: '{msg}' (length: {len(msg)} chars)"
        )
        await bot.highrise.send_whisper(user.id, msg)
        print(f"Sent feedback message to {user.username}: '{msg}'")
        await asyncio.sleep(0.5)
    except Exception as e:
        print(f"Error sending feedback message to {user.username}: {e}")
        await bot.highrise.send_whisper(user.id, f"❌ Error: {e}")
