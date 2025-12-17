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
from teleport_manager import load_teleports

tip_lock = asyncio.Lock()

highriseroomID = ROOM_ID


async def vip(bot: BaseBot, user: User, message: str) -> None:
    try:
        tips_data = load_tips()
        username = user.username.lower()
        user_data = tips_data.get(username, {"amount": 0, "vip": False})
        amount = user_data["amount"]
        is_vip = user_data["vip"]

        # Load all teleports
        teleports = load_teleports()
        vip_teleports = [
            name for name, data in teleports.items()
            if "vip" in [role.lower() for role in data.get("roles", [])]
        ]

        if is_vip:
            reply = (
                f"🌟 You are a VIP! You've tipped a total of {amount}G. Thank you!\n\n"
                "VIP Commands:\n"
                "💎 !viplist: List all VIP users")
            if vip_teleports:
                reply += "\n\n📍 **VIP Custom Teleports:**\n"
                for tp in vip_teleports:
                    reply += f"🔹 {tp}\n"
            else:
                reply += "\n\n📭 No VIP custom teleports found."
        else:
            remaining = VIP_THRESHOLD - amount
            reply = (f"💸 You're not a VIP yet. You've tipped {amount}G.\n"
                     f"Tip {remaining}G more to become a VIP!")

        await bot.highrise.send_whisper(user.id, reply)
        await asyncio.sleep(0.5)
    except Exception as e:
        print(f"Error sending VIP status: {e}")
        await bot.highrise.send_whisper(user.id,
                                        f"❌ Error checking VIP status: {e}")
    return