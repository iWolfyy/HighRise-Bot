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


async def unban(bot: BaseBot, user: User, message: str) -> None:
    try:
        try:
            room = await bot.webapi.get_room(highriseroomID)
            print(room)
            ownerID = room.room.owner_id
            room_priv = await bot.highrise.get_room_privilege(user.id)
            if not room_priv.moderator and ownerID != user.id:
                await bot.highrise.send_whisper(
                    user.id, "You need moderator privileges to use !unban.")
                return
        except Exception as e:
            await bot.highrise.send_whisper(user.id,
                                            f"Error checking privileges: {e}")
            print(f"Unban privilege check error: {e}")
            return
        parts = message.split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(user.id,
                                            "Usage: !unban <@username>")
            return
        target_username = parts[1][1:].lower()
        match = await find_user(bot, target_username)
        if not match:
            await bot.highrise.send_whisper(
                user.id, f"User @{target_username} not found.")
            return
        target_user, *_ = match  # Unpack user and ignore rest
        try:
            await bot.highrise.moderate_room(target_user.id, "unban", None)
            await bot.highrise.send_whisper(user.id,
                                            f"Unbanned @{target_username}.")
            await asyncio.sleep(0.5)
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error unbanning @{target_username}: {e}")
            print(f"Unban error: {e}")
    except Exception as e:
        await bot.highrise.send_whisper(
            user.id, f"Unexpected error processing !unban: {e}")
        print(f"Unexpected unban command error: {e}")
    return
