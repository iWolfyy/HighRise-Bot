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


async def help(bot: BaseBot, user: User, message: str) -> None:
    """Sends a help menu to the user via whispers."""
    try:
        messages = [
            "General:\n🔔 !help: Show help\n💃 !emote: List emotes\n🗣 !feedback: Contact @Mr_Wolfy\n👑 !vip: VIP status\n💎 !viplist: List VIPs\n🔧 !mod: Mod commands\n🌀 !other: Other command\n🤖!ask: Talk with the Bot.",
            "Movement:\n🚀 !tp @user: Teleport\n📍 !pos @user: Get pos\n🪄 !summon @user: Summon\n🌍 f1: F1 pos\n🔄 reset: Default pos\n📍 !viptp: VIP teleport",
            "Outfit:\n👕 !equip <item> [index]: Equip\n👗 !unequip <cat>: Unequip\n🎨 !change <cat> <color>: Change color",
            "Emotes:\n🎭 <emote>: Play emote (e.g., rest, zombie)\n🛑 stop: Stop emote"
        ]

        # Load custom teleports
        teleports = load_teleports()
        if teleports:
            msg = "📍 **Custom Teleports**\n\n"
            for name, data in teleports.items():
                roles = data.get("roles", [])
                if not roles:
                    role_display = "🌐 Everyone"
                else:
                    role_emojis = []
                    for role in roles:
                        if role == "owner":
                            role_emojis.append("👑 Owner")
                        elif role == "mod":
                            role_emojis.append("🛡️ Mod")
                        elif role == "vip":
                            role_emojis.append("💎 VIP")
                    role_display = ", ".join(role_emojis)
                msg += f"🔹 **{name}** — {role_display}\n"
            # Append this custom teleport list as last message
            messages.append(msg)

        # Send each help section as a whisper with a delay
        for msg in messages:
            if len(msg) > 280:
                print(f"Warning: Whisper message too long ({len(msg)} chars)")
            await bot.highrise.send_whisper(user.id, msg)
            await asyncio.sleep(1)

    except Exception as e:
        print(f"Error sending help message: {e}")
        await bot.highrise.send_whisper(user.id, f"❌ Error: {e}")
