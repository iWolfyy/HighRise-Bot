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
from tip_manager import load_tips, add_tip, give_vip, remove_vip, save_tips
from config import BOT_ID, ROOM_ID, BOT_UID, BOT_START_POSITION, VIP_THRESHOLD

tip_lock = asyncio.Lock()

highriseroomID = ROOM_ID


async def removevip(bot: BaseBot, user: User, message: str) -> None:
    try:
        room = await bot.webapi.get_room(highriseroomID)
        ownerID = room.room.owner_id
        if user.id != ownerID:
            await bot.highrise.send_whisper(
                user.id, "❌ You need to be the Room Owner to use !removevip.")
            return

        parts = message.split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(user.id,
                                            "Usage: !removevip <@username>")
            return

        target_username = parts[1][1:].lower()
        match = await find_user(bot, target_username)
        if not match:
            await bot.highrise.send_whisper(
                user.id, f"❌ User @{target_username} not found.")
            return

        target_user, _, _, _, _ = match

        # Remove VIP status
        success = remove_vip(target_user.username)
        if success:
            # Reset tip amount to 0
            data = load_tips()
            username_key = target_user.username.lower()
            if username_key in data:
                data[username_key]["amount"] = 0
                save_tips(data)

            await bot.highrise.send_whisper(
                user.id,
                f"✅ VIP status removed from @{target_user.username} and tip count reset."
            )
            await bot.highrise.send_whisper(
                target_user.id,
                "⚠️ Your VIP status has been removed and your tips have been reset to 0."
            )
        else:
            await bot.highrise.send_whisper(
                user.id,
                f"⚠️ @{target_user.username} has no VIP status or data.")
    except Exception as e:
        await bot.highrise.send_whisper(user.id,
                                        f"❌ Error processing !removevip: {e}")
        print(f"!removevip error: {e}")
    return
