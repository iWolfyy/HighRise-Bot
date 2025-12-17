from highrise import *
from highrise.webapi import *
from highrise.models_webapi import *
from highrise.models import *
import asyncio
import random
from config import BOT_ID, ROOM_ID, BOT_UID, BOT_START_POSITION, WEBHOOK_URL
from tip_manager import add_tip
import aiohttp
from reminder_manager import start_reminder_loop


async def on_start(bot, session_metadata: SessionMetadata) -> None:
    try:
        try:
            position = Position(x=BOT_START_POSITION["x"],
                                y=BOT_START_POSITION["y"],
                                z=BOT_START_POSITION["z"],
                                facing=BOT_START_POSITION["facing"])
            await bot.highrise.walk_to(position)
        except Exception as e:
            print(f"Error walking to position: {e}")
        await asyncio.sleep(0.5)
        try:
            asyncio.create_task(start_reminder_loop(bot))
        except Exception as e:
            print(f"Error starting reminder loop: {e}")
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
        if receiver.id != BOT_UID:
            return
        add_tip(sender.username, tip.amount)
        await bot.highrise.send_whisper(
            sender.id, f"Thanks for the tip of {tip.amount}G!")
    except Exception as e:
        print(f"Error in on_tip: {e}")


async def on_message(self, user_id: str, conversation_id: str,
                     is_new_conversation: bool) -> None:
    username = "Unknown"
    try:
        user_response = await self.webapi.get_user(user_id)
        username = getattr(user_response.user, "username", None)
        if not username:
            username = getattr(user_response.user, "display_name", None)
        if not username:
            username = getattr(user_response.user, "name", "Unknown")
    except Exception as e:
        print(f"Failed to get user info: {e}")

    try:
        response = await self.highrise.get_messages(conversation_id)
    except Exception as e:
        print(f"Failed to get messages: {e}")
        return

    message = None
    try:
        if isinstance(response, GetMessagesRequest.GetMessagesResponse):
            if response.messages and len(response.messages) > 0:
                message = response.messages[0].content
            else:
                print("No messages found.")
                return
        else:
            print("Unexpected response type.")
            return
    except Exception as e:
        print(f"Error processing messages: {e}")
        return

    print(f"Received message from {username}: {message}")

    content = (f"User: {username} (ID: {user_id})\n"
               f"Conversation ID: {conversation_id}\n"
               f"New Conversation: {is_new_conversation}\n"
               f"Message: {message}")

    try:
        async with aiohttp.ClientSession() as session:
            webhook_data = {"content": content}
            async with session.post(WEBHOOK_URL, json=webhook_data) as resp:
                if resp.status == 204:
                    print("Message sent to Discord webhook.")
                    await self.highrise.send_message(
                        conversation_id,
                        "✨ Message successfully delivered to @Mr_Wolfy! 🙏 Thanks for hitting us up "
                    )
                else:
                    print(f"Webhook failed: HTTP {resp.status}")
    except Exception as e:
        print(f"Error sending webhook: {e}")