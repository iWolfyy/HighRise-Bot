from highrise import User, Position
from highrise.models import CurrencyItem, Item
import asyncio
import requests
import random
import os
import re
from utils import find_user
import json

TIPS_FILE = "tips.json"


def load_tips():
    if not os.path.exists(TIPS_FILE):
        return {}
    with open(TIPS_FILE, "r") as file:
        return json.load(file)


def save_tips(data):
    with open(TIPS_FILE, "w") as file:
        json.dump(data, file, indent=4)


def add_tip(username, amount):
    data = load_tips()

    # If user doesn't exist, initialize
    if username not in data:
        data[username] = {"amount": 0, "vip": False}

    # Add amount to user
    data[username]["amount"] += amount

    # Update VIP status
    data[username]["vip"] = data[username]["amount"] > 500

    save_tips(data)


highriseroomID = "6871334bd8cf4ac550f0d6f7"


async def handle_command(bot, user: User, message: str) -> None:
    bot_id = os.getenv(
        "HIGHRISE_BOT_ID",
        "fda07293a4522efaef4f8e60222a6900c2575f9c05c0336c4c2a77a4502e434a")
    room_id = os.getenv("HIGHRISE_ROOM_ID", "6871334bd8cf4ac550f0d6f7")
    _id = f"1_on_1:{bot_id}:{user.id}"
    _idx = f"1_on_1:{user.id}:{bot_id}"

    if message.lower().lstrip().startswith(("!help", "-help")):
        try:
            await bot.highrise.chat(
                f"General: 🔔 !help: Show help, !emote: List emotes, !feedback: Send feedback"
            )
            await bot.highrise.chat(
                f"User Actions: 🤝 !invite: Invite, 🎸 !punk: Play guitar, ⚔️ !fight: Fight/heart/uwu, 👏 !clap: Clap/thumbs-up/wave/wink/heart"
            )
            await bot.highrise.chat(
                "Movement: 🚀 !tp: Teleport to, 📍 !pos: Get position, 🪄 !summon: Summon, 🌍 f1, f2, f3: Predefined teleports, 🔄 reset: Default position"
            )
            await bot.highrise.chat(
                "Moderator: 🔨 !kick: Kick, 🚫 !ban: Ban, 🔇 !mute: Mute, ✅ !unban: Unban, 🔍 !test: Check privileges"
            )
            await bot.highrise.chat(
                "Emotes: 🎭 <emote>: Loop (e.g., rest, zombie), 🛑 stop: End emote"
            )
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Error sending help message: {e}")
        return

    if message.lower().lstrip().startswith(("!invite", "-invite")):
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

    if message.lower().lstrip().startswith(("!feedback", "-feedback")):
        try:
            await bot.highrise.send_message(
                _id,
                "• [ Submit Feedback ]\nThank you for joining our room! We value your opinions. Please share your feedback/suggestions with @Mr_Wolfy to help improve our community. Your contributions are valuable and will help us grow.\nHave a great day!",
                "text")
            await asyncio.sleep(0.5)
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error sending feedback message: {e}")
            print(f"Feedback error: {e}")
        return

    if message.lower().lstrip().startswith(
        ("!fight", "-fight", "!uwu", "-uwu", "!punk", "-punk")):
        try:
            parts = message.split()
            command = parts[0][1:].lower()
            if len(parts) < 2 or not parts[1].startswith("@"):
                await bot.highrise.send_whisper(
                    user.id, f"Usage: !{command} <@username>")
                return
            target_username = parts[1][1:].lower()
            match = await find_user(bot, target_username)
            if not match:
                await bot.highrise.send_whisper(
                    user.id, f"User @{target_username} not found.")
                return
            target_user, _ = match
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
        return

    if message.lower().strip() == "!change":
        try:
            shirt = [
                "shirt-n_room12019casualshirt", "shirt-n_room22019formalshirt"
            ]
            pant = ["pants-n_room12019jeans", "pants-n_room22019slacks"]
            item_top = random.choice(shirt)
            item_bottom = random.choice(pant)
            try:
                await bot.highrise.set_outfit(outfit=[
                    Item(type='clothing',
                         amount=1,
                         id='body-flesh',
                         account_bound=False,
                         active_palette=65),
                    Item(type='clothing',
                         amount=1,
                         id=item_top,
                         account_bound=False,
                         active_palette=-1),
                    Item(type='clothing',
                         amount=1,
                         id=item_bottom,
                         account_bound=False,
                         active_palette=-1),
                    Item(type='clothing',
                         amount=1,
                         id='nose-n_01',
                         account_bound=False,
                         active_palette=-1),
                    Item(type='clothing',
                         amount=1,
                         id='watch-n_room32019blackwatch',
                         account_bound=False,
                         active_palette=-1),
                    Item(type='clothing',
                         amount=1,
                         id='glasses-n_room12019circleframes',
                         account_bound=False,
                         active_palette=-1),
                    Item(type='clothing',
                         amount=1,
                         id='shoes-n_room12019sneakersblack',
                         account_bound=False,
                         active_palette=-1),
                    Item(type='clothing',
                         amount=1,
                         id='mouth-basic2018downturnedthinround',
                         account_bound=False,
                         active_palette=0),
                    Item(type='clothing',
                         amount=1,
                         id='hair_front-n_malenew07',
                         account_bound=False,
                         active_palette=1),
                    Item(type='clothing',
                         amount=1,
                         id='hair_back-n_malenew07',
                         account_bound=False,
                         active_palette=1),
                    Item(type='clothing',
                         amount=1,
                         id='bag-n_room12019backpack',
                         account_bound=False,
                         active_palette=-1),
                    Item(type='clothing',
                         amount=1,
                         id='eye-n_basic2018zanyeyes',
                         account_bound=False,
                         active_palette=-1),
                    Item(type='clothing',
                         amount=1,
                         id='eyebrow-n_basic2018newbrows09',
                         account_bound=False,
                         active_palette=-1)
                ])
                await bot.highrise.chat("Outfit changed successfully!")
            except Exception as e:
                await bot.highrise.send_whisper(user.id,
                                                f"Error changing outfit: {e}")
                print(f"Outfit change error: {e}")
            await asyncio.sleep(0.5)
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Unexpected error changing outfit: {e}")
            print(f"Unexpected outfit error: {e}")
        return

    if message.lower().lstrip().startswith(("!ask", "-ask")):
        try:
            await bot.highrise.chat("You wanna mess with me lil bro?")
            await asyncio.sleep(0.5)
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error sending ask response: {e}")
            print(f"Ask error: {e}")
        return

    if message.lower().lstrip().startswith(("f1", "!f1", "-f1")):
        try:
            position = Position(x=2, y=0, z=6.5, facing="FrontLeft")
            await bot.highrise.teleport(user.id, position)
            await bot.highrise.send_whisper(user.id,
                                            "Teleported to F1 position.")
            await asyncio.sleep(0.5)
        except Exception as e:
            await bot.highrise.send_whisper(user.id,
                                            f"Error teleporting to F1: {e}")
            print(f"F1 teleport error: {e}")
        return

    if message.lower().lstrip().startswith(("f2", "!f2", "-f2")):
        try:
            position = Position(x=2, y=5, z=6.5, facing="FrontLeft")
            await bot.highrise.teleport(user.id, position)
            await bot.highrise.send_whisper(user.id,
                                            "Teleported to F2 position.")
            await asyncio.sleep(0.5)
        except Exception as e:
            await bot.highrise.send_whisper(user.id,
                                            f"Error teleporting to F2: {e}")
            print(f"F2 teleport error: {e}")
        return

    if message.lower().lstrip().startswith(("f3", "!f3", "-f3")):
        try:
            position = Position(x=6.5, y=10, z=6, facing="FrontLeft")
            await bot.highrise.teleport(user.id, position)
            await bot.highrise.send_whisper(user.id,
                                            "Teleported to F3 position.")
            await asyncio.sleep(0.5)
        except Exception as e:
            await bot.highrise.send_whisper(user.id,
                                            f"Error teleporting to F3: {e}")
            print(f"F3 teleport error: {e}")
        return

    if message.lower().lstrip().startswith(("reset", "!reset", "-reset")):
        try:
            position = Position(x=0, y=0, z=0, facing="FrontLeft")
            await bot.highrise.teleport(user.id, position)
            await bot.highrise.send_whisper(user.id,
                                            "Teleported to default position.")
            await asyncio.sleep(0.5)
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error teleporting to default: {e}")
            print(f"Reset teleport error: {e}")
        return

    if message.lower().lstrip().startswith(("!pos", "-pos")):
        try:
            parts = message.split()
            if len(parts) < 2 or not parts[1].startswith("@"):
                await bot.highrise.send_whisper(user.id,
                                                "Usage: !pos <@username>")
                return
            target_username = parts[1][1:].lower()
            match = await find_user(bot, target_username)
            if not match:
                await bot.highrise.send_whisper(
                    user.id, f"User @{target_username} not found.")
                return
            target_user, position = match
            await bot.highrise.send_whisper(
                user.id,
                f"@{target_username}'s position:\nX={position.x}, Y={position.y}, Z={position.z}"
            )
            await asyncio.sleep(0.5)
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error getting position for @{target_username}: {e}")
            print(f"Pos error: {e}")
        return

    if message.lower().lstrip().startswith(("!tp", "-tp")):
        try:
            parts = message.split()
            if len(parts) < 2 or not parts[1].startswith("@"):
                await bot.highrise.send_whisper(user.id,
                                                "Usage: !tp <@username>")
                return

            target_username = parts[1][1:].lower()
            match = await find_user(bot, target_username)

            if not match:
                await bot.highrise.send_whisper(
                    user.id, f"User @{target_username} not found.")
                return

            target_user, target_position = match

            if not target_position:
                await bot.highrise.send_whisper(
                    user.id,
                    f"Could not retrieve @{target_username}'s position.")
                return

            # Use their exact coordinates with desired facing
            exact_position = Position(
                x=target_position.x,
                y=target_position.y,
                z=target_position.z,
                facing=target_position.facing or "FrontLeft"  # fallback facing
            )

            await bot.highrise.teleport(user.id, exact_position)
            await bot.highrise.send_whisper(
                user.id, f"Teleported to @{target_username}.")
            await asyncio.sleep(0.5)

        except Exception as e:
            await bot.highrise.send_whisper(user.id,
                                            f"Error processing !tp: {e}")
            print(f"Teleport command error: {e}")
        return

    if message.lower().lstrip().startswith(("!summon", "-summon")):
        try:
            parts = message.split()
            if len(parts) < 2 or not parts[1].startswith("@"):
                await bot.highrise.send_whisper(user.id,
                                                "Usage: !summon <@username>")
                return
            target_username = parts[1][1:].lower()
            self_user_tuple = await find_user(bot, user.username)
            if not self_user_tuple:
                await bot.highrise.send_whisper(
                    user.id, "Your position couldn't be found.")
                return
            _, your_position = self_user_tuple
            match = await find_user(bot, target_username)
            if not match:
                await bot.highrise.send_whisper(
                    user.id, f"User @{target_username} not found.")
                return
            target_user, _ = match
            try:
                await bot.highrise.teleport(target_user.id, your_position)
                await bot.highrise.send_whisper(
                    user.id, f"Summoned @{target_username} to your location.")
                await bot.highrise.send_whisper(
                    target_user.id, f"@{user.username} summoned you!")
                await asyncio.sleep(0.5)
            except Exception as e:
                await bot.highrise.send_whisper(
                    user.id, f"Error summoning @{target_username}: {e}")
                print(f"Summon error: {e}")
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Unexpected error processing !summon: {e}")
            print(f"Unexpected summon command error: {e}")
        return

    if message.lower().lstrip().startswith(("!heart", "-heart")):
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
            target_user, _ = match
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
        return

    if message.lower().lstrip().startswith(("!clap", "-clap")):
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
            target_user, _ = match
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
        return

    if message.lower().lstrip().startswith(("!thumbsup", "-thumbsup")):
        try:
            parts = message.split()
            if len(parts) < 2 or not parts[1].startswith("@"):
                await bot.highrise.send_whisper(
                    user.id, "Usage: !thumbsup <@username>")
                return
            target_username = parts[1][1:].lower()
            match = await find_user(bot, target_username)
            if not match:
                await bot.highrise.send_whisper(
                    user.id, f"User @{target_username} not found.")
                return
            target_user, _ = match
            try:
                await bot.highrise.react("thumbs-up", target_user.id)
                await bot.highrise.send_whisper(
                    user.id, f"Sent a Thumbs Up to @{target_username}.")
                await bot.highrise.send_whisper(
                    target_user.id, f"@{user.username} sent you a Thumbs Up 👍")
                await asyncio.sleep(0.5)
            except Exception as e:
                await bot.highrise.send_whisper(
                    user.id,
                    f"Error sending thumbs-up to @{target_username}: {e}")
                print(f"Thumbsup error: {e}")
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Unexpected error processing !thumbsup: {e}")
            print(f"Unexpected thumbsup command error: {e}")
        return

    if message.lower().lstrip().startswith(("!wave", "-wave")):
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
            target_user, _ = match
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
        return

    if message.lower().lstrip().startswith(("!wink", "-wink")):
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
            target_user, _ = match
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
        return

    if message.lower().lstrip().startswith(("!kick", "-kick")):
        try:
            try:
                room = await bot.webapi.get_room(highriseroomID)
                print(room)
                ownerID = room.room.owner_id
                room_priv = await bot.highrise.get_room_privilege(user.id)
                if not room_priv.moderator and ownerID != user.id:
                    await bot.highrise.send_whisper(
                        user.id, "You need moderator privileges to use !kick.")
                    return
            except Exception as e:
                await bot.highrise.send_whisper(
                    user.id, f"Error checking privileges: {e}")
                print(f"Kick privilege check error: {e}")
                return
            parts = message.split()
            if len(parts) < 2 or not parts[1].startswith("@"):
                await bot.highrise.send_whisper(user.id,
                                                "Usage: !kick <@username>")
                return
            target_username = parts[1][1:].lower()
            match = await find_user(bot, target_username)
            if not match:
                await bot.highrise.send_whisper(
                    user.id, f"User @{target_username} not found.")
                return
            target_user, _ = match
            try:
                await bot.highrise.moderate_room(target_user.id, "kick", None)
                await bot.highrise.send_whisper(user.id,
                                                f"Kicked @{target_username}.")
                await asyncio.sleep(0.5)
            except Exception as e:
                await bot.highrise.send_whisper(
                    user.id, f"Error kicking @{target_username}: {e}")
                print(f"Kick error: {e}")
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Unexpected error processing !kick: {e}")
            print(f"Unexpected kick command error: {e}")
        return

    if message.lower().lstrip().startswith(("!ban", "-ban")):
        try:
            try:
                room = await bot.webapi.get_room(highriseroomID)
                print(room)
                ownerID = room.room.owner_id
                room_priv = await bot.highrise.get_room_privilege(user.id)
                if not room_priv.moderator and ownerID != user.id:
                    await bot.highrise.send_whisper(
                        user.id, "You need moderator privileges to use !ban.")
                    return
            except Exception as e:
                await bot.highrise.send_whisper(
                    user.id, f"Error checking privileges: {e}")
                print(f"Ban privilege check error: {e}")
                return
            parts = message.split()
            if len(parts) < 2 or not parts[1].startswith("@"):
                await bot.highrise.send_whisper(user.id,
                                                "Usage: !ban <@username>")
                return
            target_username = parts[1][1:].lower()
            match = await find_user(bot, target_username)
            if not match:
                await bot.highrise.send_whisper(
                    user.id, f"User @{target_username} not found.")
                return
            target_user, _ = match
            try:
                await bot.highrise.moderate_room(target_user.id, "ban", None)
                await bot.highrise.send_whisper(user.id,
                                                f"Banned @{target_username}.")
                await asyncio.sleep(0.5)
            except Exception as e:
                await bot.highrise.send_whisper(
                    user.id, f"Error banning @{target_username}: {e}")
                print(f"Ban error: {e}")
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Unexpected error processing !ban: {e}")
            print(f"Unexpected ban command error: {e}")
        return

    if message.lower().lstrip().startswith(("!mute", "-mute")):
        try:
            try:
                room_priv = await bot.highrise.get_room_privilege(user.id)
                room = await bot.webapi.get_room(highriseroomID)
                print(room)
                ownerID = room.room.owner_id
                if not room_priv.moderator and ownerID != user.id:
                    await bot.highrise.send_whisper(
                        user.id, "You need moderator privileges to use !mute.")
                    return
            except Exception as e:
                await bot.highrise.send_whisper(
                    user.id, f"Error checking privileges: {e}")
                print(f"Mute privilege check error: {e}")
                return
            parts = message.split()
            if len(parts) < 2 or not parts[1].startswith("@"):
                await bot.highrise.send_whisper(user.id,
                                                "Usage: !mute <@username>")
                return
            target_username = parts[1][1:].lower()
            match = await find_user(bot, target_username)
            if not match:
                await bot.highrise.send_whisper(
                    user.id, f"User @{target_username} not found.")
                return
            target_user, _ = match
            try:
                await bot.highrise.moderate_room(target_user.id, "mute", None)
                await bot.highrise.send_whisper(user.id,
                                                f"Muted @{target_username}.")
                await asyncio.sleep(0.5)
            except Exception as e:
                await bot.highrise.send_whisper(
                    user.id, f"Error muting @{target_username}: {e}")
                print(f"Mute error: {e}")
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Unexpected error processing !mute: {e}")
            print(f"Unexpected mute command error: {e}")
        return

    if message.lower().lstrip().startswith(("!unban", "-unban")):
        try:
            try:
                room = await bot.webapi.get_room(highriseroomID)
                print(room)
                ownerID = room.room.owner_id
                room_priv = await bot.highrise.get_room_privilege(user.id)
                if not room_priv.moderator and ownerID != user.id:
                    await bot.highrise.send_whisper(
                        user.id,
                        "You need moderator privileges to use !unban.")
                    return
            except Exception as e:
                await bot.highrise.send_whisper(
                    user.id, f"Error checking privileges: {e}")
                print(f"Unban privilege check error: {e}")
                return
            parts = message.split()
            if len(parts) < 2 or not parts[1].startswith("@"):
                await bot.highrise.send_whisper(user.id,
                                                "Usage: !unban <@username>")
                return
            target_username = parts[1][1:].lower()
            match = await find_user(bot, target_username)
            if not match:
                await bot.highrise.send_whisper(
                    user.id, f"User @{target_username} not found.")
                return
            target_user, _ = match
            try:
                await bot.highrise.moderate_room(target_user.id, "unban", None)
                await bot.highrise.send_whisper(
                    user.id, f"Unbanned @{target_username}.")
                await asyncio.sleep(0.5)
            except Exception as e:
                await bot.highrise.send_whisper(
                    user.id, f"Error unbanning @{target_username}: {e}")
                print(f"Unban error: {e}")
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Unexpected error processing !unban: {e}")
            print(f"Unexpected unban command error: {e}")
        return

    if message.lower().lstrip().startswith(("!test", "-test")):
        try:
            parts = message.split()
            if len(parts) < 2 or not parts[1].startswith("@"):
                await bot.highrise.send_whisper(user.id,
                                                "Usage: !test <@username>")
                return

            target_username = parts[1][1:].lower()
            match = await find_user(bot, target_username)
            if not match:
                await bot.highrise.send_whisper(
                    user.id, f"User @{target_username} not found.")
                return

            target_user, _ = match
            room = await bot.webapi.get_room(highriseroomID)
            print(room)
            ownerID = room.room.owner_id
            try:
                room_priv = await bot.highrise.get_room_privilege(
                    target_user.id)
                print(room_priv)

                if room_priv.moderator or ownerID == target_user.id:
                    await bot.highrise.send_whisper(
                        user.id, f"@{target_user.username} is a Moderator.")
                else:
                    await bot.highrise.send_whisper(
                        user.id,
                        f"@{target_user.username} is NOT a Moderator.")

                if room_priv.designer or ownerID == target_user.id:
                    await bot.highrise.send_whisper(
                        user.id, f"@{target_user.username} is a Designer.")
                else:
                    await bot.highrise.send_whisper(
                        user.id, f"@{target_user.username} is NOT a Designer.")

                await asyncio.sleep(0.5)

            except Exception as e:
                await bot.highrise.send_whisper(
                    user.id,
                    f"Error checking privileges for @{target_username}: {e}")
                print(f"Test privilege check error: {e}")

        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Unexpected error processing !test: {e}")
            print(f"Unexpected test command error: {e}")
        return

    if message.lower().lstrip().startswith(("!bal", "-bal")):
        try:
            parts = message.split()
            user.username = parts[1][1:].lower()
            match = await find_user(bot, user.username)
            if not match:
                await bot.highrise.send_whisper(user.id,
                                                f"User @{user} not found.")
                return
            user, _ = match
            try:
                room_priv = await bot.highrise.get_room_privilege(user.id)
                if room_priv.moderator:
                    try:
                        # Get user wallet
                        wallet = await bot.highrise.get_wallet()
                        # Find the gold amount in wallet.content
                        gold_amount = 0
                        for item in wallet.content:
                            if item.type == 'gold':
                                gold_amount = item.amount
                                break
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
                    user.id, f"Error checking privileges for @{user}: {e}")
                print(f"Test privilege check error: {e}")
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Unexpected error processing !bal: {e}")
            print(f"Unexpected test command error: {e}")
        return

    if message.lower().lstrip().startswith(("!tip", "-tip")):
        try:
            parts = message.split()
            user.username = parts[1][1:].lower()
            match = await find_user(bot, user.username)
            if not match:
                await bot.highrise.send_whisper(user.id,
                                                f"User @{user} not found.")
                return
            user, _ = match
            try:
                room_priv = await bot.highrise.get_room_privilege(user.id)
                if room_priv.moderator:
                    if message.lower().lstrip().startswith(("!tip", "-tip")):
                        try:
                            # Match the !tip command with valid amounts
                            tip_match = re.match(
                                r"!tip\s+(1|5|10|50|100|500|1000|5000|10000)\b",
                                message, re.IGNORECASE)
                            if not tip_match:
                                await bot.highrise.send_whisper(
                                    user.id,
                                    "Usage: !tip <amount> (Valid amounts: 1, 5, 10, 50, 100, 500, 1000, 5000, 10000)"
                                )
                                return
                            amount = int(tip_match.group(1))
                            try:
                                # Get bot's wallet balance
                                bot_wallet = await bot.highrise.get_wallet()
                                bot_amount = bot_wallet.content[
                                    0].amount if bot_wallet.content else 0
                                print(
                                    f"Tip wallet check: bot_amount={bot_amount}, wallet_content={bot_wallet.content}"
                                )
                                # Define gold bars and fees
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
                                # Get the list of users in the room
                                room_users = await bot.highrise.get_room_users(
                                )
                                user_ids = [
                                    u.id for u, _ in room_users.content
                                ]
                                print(f"Tip room users: user_ids={user_ids}")
                                # Remove the sender and bot from the list to avoid self-tipping
                                if user.id in user_ids:
                                    user_ids.remove(user.id)
                                if bot_id in user_ids:
                                    user_ids.remove(bot_id)
                                if not user_ids:
                                    await bot.highrise.send_whisper(
                                        user.id,
                                        "No other users in the room to tip.")
                                    print(
                                        "Tip failed: No eligible users to tip."
                                    )
                                    return
                                # Calculate total cost (amount + fee per user) for all users
                                total_per_user = 0
                                tip = []
                                temp_amount = amount
                                for bar in bars_dictionary:
                                    if temp_amount >= bar:
                                        bar_amount = temp_amount // bar
                                        temp_amount = temp_amount % bar
                                        for _ in range(bar_amount):
                                            tip.append(bars_dictionary[bar])
                                            total_per_user += bar + fees_dictionary[
                                                bar]
                                print(
                                    f"Tip calculation: amount={amount}, tip_items={tip}, total_per_user={total_per_user}, total_users={len(user_ids)}"
                                )
                                if total_per_user * len(user_ids) > bot_amount:
                                    await bot.highrise.send_whisper(
                                        user.id,
                                        "Not enough funds to tip all users.")
                                    print(
                                        f"Tip failed: Insufficient funds, required={total_per_user * len(user_ids)}, available={bot_amount}"
                                    )
                                    return
                                tip_string = ",".join(tip)
                                print(f"Tip string: {tip_string}")
                                # Send tip to each user
                                for target_user_id in user_ids:
                                    try:
                                        await bot.highrise.tip_user(
                                            target_user_id, tip_string)
                                        print(
                                            f"Tip sent: user_id={target_user_id}, tip_string={tip_string}"
                                        )
                                        await asyncio.sleep(2)
                                    except Exception as e:
                                        print(
                                            f"Tip error for user_id={target_user_id}: tip_string={tip_string}, error={e}"
                                        )
                                        await bot.highrise.send_whisper(
                                            user.id,
                                            f"Failed to tip user_id={target_user_id}: {e}"
                                        )
                                # Send confirmation message to the room
                                await bot.highrise.chat(
                                    f"Tipped Everyone in the Room {amount}.")
                                await asyncio.sleep(0.5)
                            except Exception as e:
                                await bot.highrise.send_whisper(
                                    user.id, f"Error tipping users: {e}")
                                print(f"Tip error: {e}")
                        except Exception as e:
                            await bot.highrise.send_whisper(
                                user.id,
                                f"Unexpected error processing !tip: {e}")
                            print(f"Unexpected tip command error: {e}")
                        return
                else:
                    await bot.highrise.send_whisper(
                        user.id, f"@{user.username} is NOT a Moderator.")
                await asyncio.sleep(0.5)
            except Exception as e:
                await bot.highrise.send_whisper(
                    user.id, f"Error checking privileges for @{user}: {e}")
                print(f"Test privilege check error: {e}")
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Unexpected error processing !bal: {e}")
            print(f"Unexpected test command error: {e}")
        return

    if message.lower().strip() == "!vip":
        tips_data = load_tips()
        user_data = tips_data.get(user.username, {"amount": 0, "vip": False})

        amount = user_data["amount"]
        is_vip = user_data["vip"]

        if is_vip:
            reply = f"🌟 You are a VIP! You've tipped a total of {amount}G. Thank you!"
        else:
            remaining = 500 - amount
            reply = (f"💸 You're not a VIP yet. You've tipped {amount}G.\n"
                     f"Tip {remaining}G more to become a VIP!")

        await bot.highrise.send_whisper(user.id, reply)
