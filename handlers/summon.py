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


async def summon(bot: BaseBot, user: User, message: str) -> None:
    try:
        parts = message.split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(user.id,
                                            "Usage: !summon <@username>")
            return

        target_username = parts[1][1:].lower()

        # Get command user's data
        self_user_tuple = await find_user(bot, user.username)
        if not self_user_tuple:
            await bot.highrise.send_whisper(
                user.id, "Your position couldn't be found.")
            return
        _, your_position, _, _, _ = self_user_tuple

        # Get target user's data
        target_match = await find_user(bot, target_username)
        if not target_match:
            await bot.highrise.send_whisper(
                user.id, f"User @{target_username} not found.")
            return
        target_user, _, _, _, _ = target_match

        # Teleport target to your position
        try:
            await bot.highrise.teleport(target_user.id, your_position)
            await bot.highrise.send_whisper(
                user.id, f"✅ Summoned @{target_username} to your location.")
            await bot.highrise.send_whisper(
                target_user.id, f"⚠️ @{user.username} summoned you!")
            await asyncio.sleep(0.5)
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"❌ Error summoning @{target_username}: {e}")
            print(f"Summon error: {e}")

    except Exception as e:
        await bot.highrise.send_whisper(
            user.id, f"❌ Unexpected error processing !summon: {e}")
        print(f"Unexpected summon command error: {e}")
