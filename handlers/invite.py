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

async def invite(bot: BaseBot, user: User, message: str) -> None:
    try:
        parts = message.split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(
                user.id,
                "Usage: !invite <@username>\nExample: !invite @Mr_Wolfy")
            return
        target_username = parts[1][1:]
        try:
            url = f"https://webapi.highrise.game/users?&username={target_username}&sort_order=asc&limit=1"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            users = data.get('users', [])
            if not users:
                await bot.highrise.send_whisper(
                    user.id, f"User @{target_username} not found.")
                return
            target_user_id = users[0]['user_id']
            conv_id = f"1_on_1:{bot_id}:{target_user_id}"
            conv_id_alt = f"1_on_1:{target_user_id}:{bot_id}"
            try:
                await bot.highrise.send_message(conv_id, "Join Room",
                                                "invite", room_id)
                await bot.highrise.send_whisper(
                    user.id, f"Invite sent to @{target_username}.")
            except Exception:
                await bot.highrise.send_message(conv_id_alt, "Join Room",
                                                "invite", room_id)
                await bot.highrise.send_whisper(
                    user.id, f"Invite sent to @{target_username}.")
            await asyncio.sleep(0.5)
        except requests.RequestException as e:
            await bot.highrise.send_whisper(
                user.id, f"Error fetching user @{target_username}: {e}")
            print(f"Invite request error: {e}")
    except Exception as e:
        await bot.highrise.send_whisper(
            user.id,
            f"Unexpected error sending invite to @{target_username}: {e}")
        print(f"Unexpected invite error: {e}")
    return
    