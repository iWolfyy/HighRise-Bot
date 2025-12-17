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


async def tip(bot: BaseBot, user: User, message: str) -> None:
    if tip_lock.locked():
        await bot.highrise.send_whisper(user.id,
                                        "⚠️ Tip in progress. Please wait.")
        return

    async with tip_lock:
        try:
            room = await bot.webapi.get_room(highriseroomID)
            owner_id = room.room.owner_id
            room_priv = await bot.highrise.get_room_privilege(user.id)
            if owner_id != user.id:
                await bot.highrise.send_whisper(
                    user.id, "You need to be the Room Owner to be able to use this function.")
                return

            tip_match = re.match(
                r"!tip\s+(1|5|10|50|100|500|1000|5000|10000)\b", message,
                re.IGNORECASE)
            if not tip_match:
                await bot.highrise.send_whisper(
                    user.id,
                    "Usage: !tip <amount> (Valid: 1, 5, 10, 50, 100, 500, 1000, 5000, 10000)"
                )
                return

            amount = int(tip_match.group(1))

            bot_wallet = await bot.highrise.get_wallet()
            bot_amount = bot_wallet.content[
                0].amount if bot_wallet.content else 0

            bars_dictionary = {
                10000: "gold_bar_10k",
                5000: "gold_bar_5000",
                1000: "gold_bar_1k",
                500: "gold_bar_500",
                100: "gold_bar_100",
                50: "gold_bar_50",
                10: "gold_bar_10",
                5: "gold_bar_5",
                1: "gold_bar_1"
            }

            fees_dictionary = {
                10000: 1000,
                5000: 500,
                1000: 100,
                500: 50,
                100: 10,
                50: 5,
                10: 1,
                5: 1,
                1: 1
            }

            room_users = await bot.highrise.get_room_users()
            user_ids = [u.id for u, _ in room_users.content]

            user_ids = [
                uid for uid in user_ids if uid not in (user.id, BOT_UID)
            ]
            if not user_ids:
                await bot.highrise.send_whisper(
                    user.id, "No other users in the room to tip.")
                return

            tip_items = []
            temp_amount = amount
            total_per_user = 0

            for bar in sorted(bars_dictionary.keys(), reverse=True):
                while temp_amount >= bar:
                    tip_items.append(bars_dictionary[bar])
                    total_per_user += bar + fees_dictionary[bar]
                    temp_amount -= bar

            if total_per_user * len(user_ids) > bot_amount:
                await bot.highrise.send_whisper(
                    user.id, "Not enough funds to tip all users.")
                return

            tip_string = ",".join(tip_items)

            await bot.highrise.send_whisper(user.id, "✅ Tip command received.")
            await bot.highrise.send_whisper(user.id, "🔄 Tipping all users...")

            for target_user_id in user_ids:
                try:
                    target_user = next((u for u, _ in room_users.content
                                        if u.id == target_user_id), None)
                    if target_user:
                        await bot.highrise.tip_user(target_user_id, tip_string)
                        await bot.highrise.chat(
                            f"💰 Tipped @{target_user.username} {amount} Gold! 💰✨"
                        )
                        await asyncio.sleep(2)
                    else:
                        await bot.highrise.send_whisper(
                            user.id,
                            f"Could not find user with id {target_user_id}")
                except Exception as e:
                    await bot.highrise.send_whisper(
                        user.id, f"Failed to tip user {target_user_id}: {e}")
            await bot.highrise.chat(
                f"✅ Successfully tipped {len(user_ids)} users with {amount} gold."
            )
            await asyncio.sleep(0.5)

        except Exception as e:
            await bot.highrise.send_whisper(user.id, f"Unexpected error: {e}")
            print(f"Tip error: {e}")