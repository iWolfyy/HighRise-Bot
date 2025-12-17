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


async def test(bot: BaseBot, user: User, message: str) -> None:
    try:
        parts = message.split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(user.id,
                                            "Usage: !test <@username>")
            return

        target_username = parts[1][1:].lower()
        match = await find_user(bot, target_username)
        if not match:
            await bot.highrise.send_whisper(
                user.id, f"User @{target_username} not found.")
            return

        target_user, _, is_vip, is_mod, is_owner = match

        if is_owner or is_mod:
            await bot.highrise.send_whisper(
                user.id, f"@{target_user.username} is a Moderator or Owner.")
        else:
            await bot.highrise.send_whisper(
                user.id,
                f"@{target_user.username} is NOT a Moderator or Owner.")

        # Optional: Designer check (from Web API)
        try:
            room_priv = await bot.highrise.get_room_privilege(target_user.id)
            if room_priv.designer or is_owner:
                await bot.highrise.send_whisper(
                    user.id, f"@{target_user.username} is a Designer.")
            else:
                await bot.highrise.send_whisper(
                    user.id, f"@{target_user.username} is NOT a Designer.")
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error checking designer status: {e}")
            print(f"Designer check error: {e}")

        await asyncio.sleep(0.5)

    except Exception as e:
        await bot.highrise.send_whisper(
            user.id, f"Unexpected error processing !test: {e}")
        print(f"Unexpected test command error: {e}")
