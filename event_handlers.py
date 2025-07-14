from highrise.models import SessionMetadata, User, Reaction, Position, CurrencyItem, Item, GetMessagesRequest
import asyncio
import random
import json
import os

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
    data[username]["vip"] = data[username]["amount"] > 1

    save_tips(data)


async def on_start(bot, session_metadata: SessionMetadata) -> None:
    try:
        try:
            await bot.highrise.walk_to(Position(4, 0, 7.5, "FrontLeft"))
        except Exception as e:
            print(f"Error walking to position: {e}")
        try:
            await bot.highrise.chat(
                "Bot Started.\nContact @Mr_Wolfy for any issues.")
        except Exception as e:
            print(f"Error sending start message: {e}")
        await asyncio.sleep(0.5)
    except Exception as e:
        print(f"Error in on_start: {e}")


async def on_reaction(bot, user: User, reaction: Reaction,
                      receiver: User) -> None:
    try:
        text_to_emoji = {
            "göz kırpma": "😉",
            "dalga": "👋",
            "tamamdır": "👍",
            "kalp": "❤️",
            "alkış": "👏",
        }
        try:
            await bot.highrise.chat(
                f"\n{user.username} {text_to_emoji[reaction]} {receiver.username}"
            )
        except Exception as e:
            print(f"Error sending reaction message: {e}")
        await asyncio.sleep(0.5)
    except Exception as e:
        print(f"Error in on_reaction: {e}")


async def on_user_join(bot, user: User, position: Position) -> None:
    try:
        print(f"{user.username} Joined Room.")
        wm = [
            'Welcome in! Glad to have you here 🖤',
            'You made it! Kick back and vibe with us ✨',
            'Good to see you! Let the energy flow 🔥',
            'Welcome to the room! Make yourself at home 😎',
            'We’re hyped you’re here! Let’s make it a vibe 🎉',
        ]
        try:
            rwm = random.choice(wm)
            await bot.highrise.send_whisper(user.id,
                                            f"Hey {user.username}\n{rwm}")
        except Exception as e:
            print(f"Error sending welcome whisper: {e}")
        try:
            await bot.highrise.send_whisper(
                user.id, f"\n[📢] Type !help in room for Bot Info!")
        except Exception as e:
            print(f"Error sending help whisper: {e}")
        face = ["FrontRight", "FrontLeft"]
        try:
            fp = random.choice(face)
            _ = [
                Position(2, 0, 6.5, fp),
                Position(2, 5, 6.5, fp),
                Position(6.5, 10, 6, fp),
            ]
            __ = random.choice(_)
            await bot.highrise.teleport(user.id, __)
        except Exception as e:
            print(f"Error teleporting user: {e}")
            await bot.highrise.send_whisper(user.id,
                                            f"Error teleporting you: {e}")
        await asyncio.sleep(0.5)
    except Exception as e:
        print(f"Error in on_user_join: {e}")
        try:
            await bot.highrise.send_whisper(user.id,
                                            f"Error handling join: {e}")
        except Exception as e2:
            print(f"Error sending error whisper in on_user_join: {e2}")


async def on_tip(bot, sender: User, receiver: User,
                 tip: CurrencyItem | Item) -> None:
    try:
        add_tip(sender.username, tip.amount)
        await bot.highrise.send_whisper(
            sender.id, f"Thanks for the tip of {tip.amount}G!")
    except Exception as e:
        print(f"Error in on_tip: {e}")


async def on_message(self, user_id: str, conversation_id: str,
                     is_new_conversation: bool) -> None:
    response = await self.highrise.get_messages(conversation_id)
    if isinstance(response, GetMessagesRequest.GetMessagesResponse):
        message = response.messages[0].content
        if message.lower() == "!help" or message.lower() == "help":
            await self.highrise.send_message(
                conversation_id,
                f"General: 🔔 !help: Show help, !emote: List emotes, !feedback: Send feedback"
            )
            await self.highrise.send_message(
                conversation_id,
                f"User Actions: 🤝 !invite: Invite, 🎸 !punk: Play guitar, ⚔️ !fight: Fight/heart/uwu, 👏 !clap: Clap/thumbs-up/wave/wink/heart"
            )
            await self.highrise.send_message(
                conversation_id,
                f"Movement: 🚀 !tp: Teleport to, 📍 !pos: Get position, 🪄 !summon: Summon, 🌍 f1, f2, f3: Predefined teleports, 🔄 reset: Default position"
            )
            await self.highrise.send_message(
                conversation_id,
                f"Moderator: 🔨 !kick: Kick, 🚫 !ban: Ban, 🔇 !mute: Mute, ✅ !unban: Unban, 🔍 !test: Check privileges"
            )
            await self.highrise.send_message(
                conversation_id,
                f"Emotes: 🎭 <emote>: Loop (e.g., rest, zombie), 🛑 stop: End emote"
            )
