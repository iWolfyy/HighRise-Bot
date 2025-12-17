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


async def movebot(bot: BaseBot, user: User, message: str) -> None:
    try:
        # Find user info using new utils
        result = await find_user(bot, user.username)
        if not result:
            await bot.highrise.send_whisper(
                user.id, "Your user info couldn't be found.")
            return

        found_user, user_position, is_vip, is_mod, is_owner = result

        # Check mod or owner
        if not (is_mod or is_owner):
            await bot.highrise.send_whisper(
                user.id,
                "You need moderator privileges or be the room owner to use !movebot."
            )
            return

        if not user_position:
            await bot.highrise.send_whisper(
                user.id, "Your position couldn't be found.")
            return

        # Update config.py with new bot start position
        config_path = "config.py"
        with open(config_path, "r") as file:
            config_content = file.read()

        new_position = (f"    \"x\": {user_position.x},\n"
                        f"    \"y\": {user_position.y},\n"
                        f"    \"z\": {user_position.z},\n"
                        f"    \"facing\": \"{user_position.facing}\"")

        new_config_content = re.sub(
            r'BOT_START_POSITION = \{[^}]*\}',
            f'BOT_START_POSITION = {{\n{new_position}\n}}', config_content)

        with open(config_path, "w") as file:
            file.write(new_config_content)

        # Make bot walk to user position
        await bot.highrise.walk_to(user_position)
        await bot.highrise.send_whisper(
            user.id,
            f"Bot moved to your position: X={user_position.x}, Y={user_position.y}, Z={user_position.z}, Facing={user_position.facing}"
        )
        await asyncio.sleep(0.5)

    except Exception as e:
        await bot.highrise.send_whisper(user.id,
                                        f"Error processing !movebot: {e}")
        print(f"Movebot command error: {e}")
