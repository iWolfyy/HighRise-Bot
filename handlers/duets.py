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


async def duets(bot: BaseBot, user: User, message: str) -> None:
    try:
        parts = message.split()
        command = parts[0][1:].lower()

        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(user.id,
                                            f"Usage: !{command} <@username>")
            return

        target_username = parts[1][1:].lower()
        match = await find_user(bot, target_username)
        if not match:
            await bot.highrise.send_whisper(
                user.id, f"User @{target_username} not found.")
            return

        target_user, _, _, _, _ = match

        try:
            if command == "fight":
                await bot.highrise.chat(
                    f"\n🥷 @{user.username} VS @{target_username} FIGHTTTT!!!!🤺"
                )
                await bot.highrise.send_emote("emote-swordfight", user.id)
                await bot.highrise.send_emote("emote-swordfight",
                                              target_user.id)
            elif command == "uwu":
                await bot.highrise.chat(
                    f"\n@{user.username} and @{target_username} are very sweet🥺"
                )
                await bot.highrise.send_emote("idle-uwu", user.id)
                await bot.highrise.send_emote("idle-uwu", target_user.id)
            elif command == "punk":
                await bot.highrise.chat(
                    f"\nHey @{user.username} and @{target_username} ooo very cool😎🎸"
                )
                await bot.highrise.send_emote("emote-punkguitar", user.id)
                await bot.highrise.send_emote("emote-punkguitar",
                                              target_user.id)

            await asyncio.sleep(0.5)

        except Exception as e:
            await bot.highrise.send_whisper(
                user.id,
                f"Error executing {command} with @{target_username}: {e}")
            print(f"Command {command} error: {e}")

    except Exception as e:
        await bot.highrise.send_whisper(
            user.id, f"Unexpected error processing {command}: {e}")
        print(f"Unexpected error in fight/uwu/punk: {e}")
