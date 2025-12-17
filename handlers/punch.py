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


async def punch(bot: BaseBot, user: User, message: str) -> None:
    try:
        try:
            room = await bot.webapi.get_room(highriseroomID)
            print(room)
            ownerID = room.room.owner_id
            room_priv = await bot.highrise.get_room_privilege(user.id)
            if not room_priv.moderator and ownerID != user.id:
                await bot.highrise.send_whisper(
                    user.id, "You need moderator privileges to use !punch.")
                return
        except Exception as e:
            await bot.highrise.send_whisper(user.id,
                                            f"Error checking privileges: {e}")
            print(f"Punch privilege check error: {e}")
            return
        parts = message.split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(user.id,
                                            "Usage: !punch <@username>")
            return
        target_username = parts[1][1:].lower()
        match = await find_user(bot, target_username)
        if not match:
            await bot.highrise.send_whisper(
                user.id, f"User @{target_username} not found.")
            return
        target_user, _ = match
        try:
            await bot.highrise.chat(
                    f"\n@{user.username} Punched @{target_username} 👊💥"
                )
            await bot.highrise.send_emote("emote-superpunch", user.id)
            
            await bot.highrise.send_emote("emote-apart",
                                          target_user.id)
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error kicking @{target_username}: {e}")
            print(f"Kick error: {e}")
    except Exception as e:
        await bot.highrise.send_whisper(
            user.id, f"Unexpected error processing !kick: {e}")
        print(f"Unexpected kick command error: {e}")
    return
