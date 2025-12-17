from highrise import BaseBot, User
import asyncio
from utils import find_user
from config import BOT_UID

# -------------------------------------------------------
# Individual Reactions
# -------------------------------------------------------

async def heart(bot: BaseBot, user: User, message: str) -> None:
    try:
        parts = message.split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(user.id, "Usage: !heart <@username>")
            return
        target_username = parts[1][1:].lower()
        match = await find_user(bot, target_username)
        if not match:
            await bot.highrise.send_whisper(user.id, f"User @{target_username} not found.")
            return
        target_user = match[0]
        try:
            await bot.highrise.react("heart", target_user.id)
            await bot.highrise.send_whisper(user.id, f"Sent a ❤️ to @{target_username}.")
            await bot.highrise.send_whisper(target_user.id, f"@{user.username} sent you a Heart 💖")
        except Exception as e:
            await bot.highrise.send_whisper(user.id, f"Error sending heart: {e}")
    except Exception as e:
        print(f"Heart error: {e}")

async def clap(bot: BaseBot, user: User, message: str) -> None:
    try:
        parts = message.split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(user.id, "Usage: !clap <@username>")
            return
        target_username = parts[1][1:].lower()
        match = await find_user(bot, target_username)
        if not match:
            await bot.highrise.send_whisper(user.id, f"User @{target_username} not found.")
            return
        target_user = match[0]
        try:
            await bot.highrise.react("clap", target_user.id)
            await bot.highrise.send_whisper(user.id, f"Sent a Clap to @{target_username}.")
            await bot.highrise.send_whisper(target_user.id, f"@{user.username} sent you a Clap 👏🏻")
        except Exception as e:
            await bot.highrise.send_whisper(user.id, f"Error sending clap: {e}")
    except Exception as e:
        print(f"Clap error: {e}")

async def thumbsup(bot: BaseBot, user: User, message: str) -> None:
    try:
        parts = message.split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(user.id, "Usage: !thumbsup <@username>")
            return
        target_username = parts[1][1:].lower()
        match = await find_user(bot, target_username)
        if not match:
            await bot.highrise.send_whisper(user.id, f"User @{target_username} not found.")
            return
        target_user = match[0]
        try:
            await bot.highrise.react("thumbs-up", target_user.id)
            await bot.highrise.send_whisper(user.id, f"Sent a Thumbs Up to @{target_username}.")
            await bot.highrise.send_whisper(target_user.id, f"@{user.username} sent you a Thumbs Up 👍")
        except Exception as e:
            await bot.highrise.send_whisper(user.id, f"Error sending thumbsup: {e}")
    except Exception as e:
        print(f"Thumbsup error: {e}")

async def wave(bot: BaseBot, user: User, message: str) -> None:
    try:
        parts = message.split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(user.id, "Usage: !wave <@username>")
            return
        target_username = parts[1][1:].lower()
        match = await find_user(bot, target_username)
        if not match:
            await bot.highrise.send_whisper(user.id, f"User @{target_username} not found.")
            return
        target_user = match[0]
        try:
            await bot.highrise.react("wave", target_user.id)
            await bot.highrise.send_whisper(user.id, f"Sent a Wave to @{target_username}.")
            await bot.highrise.send_whisper(target_user.id, f"@{user.username} sent you a Wave 👋")
        except Exception as e:
            await bot.highrise.send_whisper(user.id, f"Error sending wave: {e}")
    except Exception as e:
        print(f"Wave error: {e}")

async def wink(bot: BaseBot, user: User, message: str) -> None:
    try:
        parts = message.split()
        if len(parts) < 2 or not parts[1].startswith("@"):
            await bot.highrise.send_whisper(user.id, "Usage: !wink <@username>")
            return
        target_username = parts[1][1:].lower()
        match = await find_user(bot, target_username)
        if not match:
            await bot.highrise.send_whisper(user.id, f"User @{target_username} not found.")
            return
        target_user = match[0]
        try:
            await bot.highrise.react("wink", target_user.id)
            await bot.highrise.send_whisper(user.id, f"Sent a Wink to @{target_username}.")
            await bot.highrise.send_whisper(target_user.id, f"@{user.username} sent you a Wink 😉")
        except Exception as e:
            await bot.highrise.send_whisper(user.id, f"Error sending wink: {e}")
    except Exception as e:
        print(f"Wink error: {e}")

# -------------------------------------------------------
# Mass Reactions
# -------------------------------------------------------

async def heart_all(bot: BaseBot, user: User, message: str) -> None:
    try:
        # Check permissions using find_user
        match = await find_user(bot, user.username)
        if not match:
            await bot.highrise.send_whisper(user.id, "Couldn't verify your permissions.")
            return

        # match returns: user_obj, user_id, username, is_mod, is_owner
        is_mod = match[3]
        is_owner = match[4]

        if not (is_mod or is_owner):
            await bot.highrise.send_whisper(user.id, "Only the room owner or a moderator can use this command.")
            return

        room_users = await bot.highrise.get_room_users()
        
        # Notify user process has started
        await bot.highrise.send_whisper(user.id, f"Sending hearts to {len(room_users.content)} users...")

        for u, pos in room_users.content:
            # Skip the user running the command and the bot itself
            if u.id not in [user.id, BOT_UID]:
                try:
                    await bot.highrise.react("heart", u.id)
                    await asyncio.sleep(0.3) # Sleep to avoid rate limits
                except Exception as e:
                    print(f"Error hearting {u.username}: {e}")

        await bot.highrise.send_whisper(user.id, "Sent ❤️ to everyone in the room.")

    except Exception as e:
        await bot.highrise.send_whisper(user.id, f"Error in !heartall: {e}")
        print(f"heart_all error: {e}")