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


async def viplist(bot: BaseBot, user: User, message: str) -> None:
    try:
        data = load_tips()
        vip_users = [user for user, info in data.items() if info.get("vip")]
        if not vip_users:
            await bot.highrise.send_whisper(user.id, "No VIPs yet.")
        else:
            chunk = ""
            for vip in vip_users:
                if len(chunk + vip + ", ") >= 280:
                    await bot.highrise.send_whisper(
                        user.id, f"💎 VIPs: {chunk.strip(', ')}")
                    await asyncio.sleep(1)
                    chunk = ""
                chunk += vip + ", "
            if chunk:
                await bot.highrise.send_whisper(
                    user.id, f"💎 VIPs: {chunk.strip(', ')}")
    except Exception as e:
        await bot.highrise.send_whisper(user.id, "Error loading VIP list.")
        print(f"Error in !viplist command: {e}")
