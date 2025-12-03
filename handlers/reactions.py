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


async def heart(bot: BaseBot, user: User, message: str) -> None:
    try:
        parts = message.split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(user.id,
                                            "Usage: !heart <@username>")
            return
        target_username = parts[1][1:].lower()
        match = await find_user(bot, target_username)
        if not match:
            await bot.highrise.send_whisper(
                user.id, f"User @{target_username} not found.")
            return
        target_user, _, _, _, _ = match
        try:
            await bot.highrise.react("heart", target_user.id)
            await bot.highrise.send_whisper(
                user.id, f"Sent a ❤️ to @{target_username}.")
            await bot.highrise.send_whisper(
                target_user.id, f"@{user.username} sent you a Heart 💖")
            await asyncio.sleep(0.5)
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error sending heart to @{target_username}: {e}")
            print(f"Heart error: {e}")
    except Exception as e:
        await bot.highrise.send_whisper(
            user.id, f"Unexpected error processing !heart: {e}")
        print(f"Unexpected heart command error: {e}")


async def clap(bot: BaseBot, user: User, message: str) -> None:
    try:
        parts = message.split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(user.id,
                                            "Usage: !clap <@username>")
            return
        target_username = parts[1][1:].lower()
        match = await find_user(bot, target_username)
        if not match:
            await bot.highrise.send_whisper(
                user.id, f"User @{target_username} not found.")
            return
        target_user, _, _, _, _ = match
        try:
            await bot.highrise.react("clap", target_user.id)
            await bot.highrise.send_whisper(
                user.id, f"Sent a Clap to @{target_username}.")
            await bot.highrise.send_whisper(
                target_user.id, f"@{user.username} sent you a Clap 👏🏻")
            await asyncio.sleep(0.5)
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error sending clap to @{target_username}: {e}")
            print(f"Clap error: {e}")
    except Exception as e:
        await bot.highrise.send_whisper(
            user.id, f"Unexpected error processing !clap: {e}")
        print(f"Unexpected clap command error: {e}")


async def thumbsup(bot: BaseBot, user: User, message: str) -> None:
    try:
        parts = message.split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(user.id,
                                            "Usage: !thumbsup <@username>")
            return
        target_username = parts[1][1:].lower()
        match = await find_user(bot, target_username)
        if not match:
            await bot.highrise.send_whisper(
                user.id, f"User @{target_username} not found.")
            return
        target_user, _, _, _, _ = match
        try:
            await bot.highrise.react("thumbs-up", target_user.id)
            await bot.highrise.send_whisper(
                user.id, f"Sent a Thumbs Up to @{target_username}.")
            await bot.highrise.send_whisper(
                target_user.id, f"@{user.username} sent you a Thumbs Up 👍")
            await asyncio.sleep(0.5)
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error sending thumbs-up to @{target_username}: {e}")
            print(f"Thumbsup error: {e}")
    except Exception as e:
        await bot.highrise.send_whisper(
            user.id, f"Unexpected error processing !thumbsup: {e}")
        print(f"Unexpected thumbsup command error: {e}")


async def wave(bot: BaseBot, user: User, message: str) -> None:
    try:
        parts = message.split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(user.id,
                                            "Usage: !wave <@username>")
            return
        target_username = parts[1][1:].lower()
        match = await find_user(bot, target_username)
        if not match:
            await bot.highrise.send_whisper(
                user.id, f"User @{target_username} not found.")
            return
        target_user, _, _, _, _ = match
        try:
            await bot.highrise.react("wave", target_user.id)
            await bot.highrise.send_whisper(
                user.id, f"Sent a Wave to @{target_username}.")
            await bot.highrise.send_whisper(
                target_user.id, f"@{user.username} sent you a Wave 👋")
            await asyncio.sleep(0.5)
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error sending wave to @{target_username}: {e}")
            print(f"Wave error: {e}")
    except Exception as e:
        await bot.highrise.send_whisper(
            user.id, f"Unexpected error processing !wave: {e}")
        print(f"Unexpected wave command error: {e}")


async def wink(bot: BaseBot, user: User, message: str) -> None:
    try:
        parts = message.split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(user.id,
                                            "Usage: !wink <@username>")
            return
        target_username = parts[1][1:].lower()
        match = await find_user(bot, target_username)
        if not match:
            await bot.highrise.send_whisper(
                user.id, f"User @{target_username} not found.")
            return
        target_user, _, _, _, _ = match
        try:
            await bot.highrise.react("wink", target_user.id)
            await bot.highrise.send_whisper(
                user.id, f"Sent a Wink to @{target_username}.")
            await bot.highrise.send_whisper(
                target_user.id, f"@{user.username} sent you a Wink 😉")
            await asyncio.sleep(0.5)
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error sending wink to @{target_username}: {e}")
            print(f"Wink error: {e}")
    except Exception as e:
        await bot.highrise.send_whisper(
            user.id, f"Unexpected error processing !wink: {e}")
        print(f"Unexpected wink command error: {e}")


async def heart_all(bot: BaseBot, user: User, message: str) -> None:
    try:
        # Get role info using find_user
        match = await find_user(bot, user.username)
        if not match:
            await bot.highrise.send_whisper(
                user.id, "Couldn't verify your permissions.")
            return

        _, _, _, is_mod, is_owner = match
        if not (is_mod or is_owner):
            await bot.highrise.send_whisper(
                user.id,
                "Only the room owner or a moderator can use this command.")
            return

        # Get all users in the room
        room_users = await bot.highrise.get_room_users()

        # Send hearts to everyone except the bot and the command sender
        for u, _ in room_users.content:
            if u.id not in [user.id, BOT_UID]:
                try:
                    await bot.highrise.react("heart", u.id)
                    await asyncio.sleep(0.3)  # Prevent hitting rate limits
                except Exception as e:
                    print(f"Error hearting {u.username}: {e}")

        await bot.highrise.send_whisper(user.id,
                                        "Sent ❤️ to everyone in the room.")

    except Exception as e:
        await bot.highrise.send_whisper(user.id, f"Error in !heartall: {e}")
        print(f"heart_all error: {e}")
