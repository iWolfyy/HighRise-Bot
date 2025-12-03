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
from teleport_manager import load_teleports  # Import your teleport loader

tip_lock = asyncio.Lock()

highriseroomID = ROOM_ID


async def other(bot: BaseBot, user: User, message: str) -> None:
    """Sends a help menu to the user via whispers."""
    try:
        messages = [
            "Fun & Info:\n😂 !joke: Get random jokes\n💸 !tax: Highrise Gold Tax Calculator\n📰 !news: Top news of the day\n🧠 !fact: Get random facts",
        ]

        # Send each help section as a whisper with a delay
        for msg in messages:
            if len(msg) > 280:
                print(f"Warning: Whisper message too long ({len(msg)} chars)")
            await bot.highrise.send_whisper(user.id, msg)
            await asyncio.sleep(1)

    except Exception as e:
        print(f"Error sending help message: {e}")
        await bot.highrise.send_whisper(user.id, f"❌ Error: {e}")
