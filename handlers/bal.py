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


async def bal(bot: BaseBot, user: User, message: str) -> None:
    try:
        match = await find_user(bot, user.username)
        if not match:
            await bot.highrise.send_whisper(
                user.id, f"User @{user.username} not found.")
            return

        found_user, _, is_vip, is_mod, is_owner = match

        if is_mod or is_owner:
            try:
                wallet = await bot.highrise.get_wallet()
                gold_amount = next(
                    (item.amount
                     for item in wallet.content if item.type == 'gold'), 0)
                await bot.highrise.send_whisper(
                    user.id, f"Your Gold Balance: {gold_amount} Gold💰")
            except Exception as e:
                await bot.highrise.send_whisper(
                    user.id, f"Error fetching balance: {str(e)}")
        else:
            await bot.highrise.send_whisper(
                user.id, f"@{user.username} is NOT a Moderator.")

        await asyncio.sleep(0.5)

    except Exception as e:
        await bot.highrise.send_whisper(
            user.id, f"Unexpected error processing !bal: {e}")
        print(f"Unexpected !bal command error: {e}")
