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

async def givevip(bot: BaseBot, user: User, message: str) -> None:
    try:
        room = await bot.webapi.get_room(highriseroomID)
        ownerID = room.room.owner_id
        if user.id != ownerID:
            await bot.highrise.send_whisper(
                user.id,
                "❌ You need to be the Room Owner to use !givevip.")
            return
        parts = message.split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(user.id,
                                            "Usage: !givevip <@username>")
            return
        target_username = parts[1][1:].lower()
        match = await find_user(bot, target_username)
        if not match:
            await bot.highrise.send_whisper(
                user.id, f"❌ User @{target_username} not found.")
            return
        target_user, _ = match
        give_vip(target_user.username)
        await bot.highrise.send_whisper(
            user.id,
            f"✅ @{target_user.username} has been granted VIP status.")
        await bot.highrise.send_whisper(
            target_user.id, "🌟 You have been granted VIP status!")
    except Exception as e:
        await bot.highrise.send_whisper(
            user.id, f"❌ Error processing !givevip: {e}")
        print(f"!givevip error: {e}")
    return
