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


async def mod(bot: BaseBot, user: User, message: str) -> None:
    """Sends moderator/owner commands to the user via whispers."""
    try:
        match = await find_user(bot, user.username)
        if not match:
            await bot.highrise.send_whisper(
                user.id, f"User @{user.username} not found.")
            return

        _, _, _, is_mod, is_owner = match
        if not (is_mod or is_owner):
            await bot.highrise.send_whisper(
                user.id, "❌ Need mod/owner privileges for !mod.")
            return

        messages = [
            "Mod Cmds:\n🔨 !kick @user: Kick\n🚫 !ban @user: Ban\n🔇 !mute @user: Mute\n✅ !unban @user: Unban\n🔍 !test @user: Check privs",
            "Mod Cmds:\n💰 !bal: Bot gold\n💸 !tip <amt>: Tip all\n🌟 !givevip @user: Grant VIP (Owner Only)\n❌ !removevip @user: Remove VIP (Owner Only) \n📍 !modtp: Mod area\n🤖 !movebot: Move bot",
            "Mod Cmds:\n📍 !maketele [telename] [roles...]: Create teleport\n📍 !deltele [Telename]: Delete teleport\n📍 !teleports: List teleports"
        ]

        for msg in messages:
            if len(msg) > 280:
                print(
                    f"Warning: Whisper message too long ({len(msg)} chars): {msg}"
                )
            await bot.highrise.send_whisper(user.id, msg)
            await asyncio.sleep(1)  # To avoid rate limiting

    except Exception as e:
        print(f"Error sending mod commands: {e}")
        await bot.highrise.send_whisper(user.id, f"❌ Error: {e}")
