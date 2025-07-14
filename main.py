from highrise import BaseBot, SessionMetadata
import asyncio
import os
from utils import find_user
from event_handlers import on_start, on_reaction, on_user_join, on_tip, on_message
from emote_manager import handle_emote_command, stop_emote
from command_handlers import handle_command
from highrise.__main__ import main as highrise_main


class Bot(BaseBot):

    def __init__(self):
        super().__init__()
        self.active_emote_loops = {
        }  # Dictionary to track active emote tasks and emote IDs per user

    async def find_user(self, username: str) -> tuple | None:
        return await find_user(self, username)

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        await on_start(self, session_metadata)

    async def on_reaction(self, user, reaction, receiver) -> None:
        await on_reaction(self, user, reaction, receiver)

    async def on_user_join(self, user, position) -> None:
        await on_user_join(self, user, position)

    async def on_tip(self, sender, receiver, tip) -> None:
        await on_tip(self, sender, receiver, tip)

    async def on_message(self, user_id, conversation_id,
                         is_new_conversation) -> None:
        await on_message(self, user_id, conversation_id, is_new_conversation)

    async def on_chat(self, user, message):
        try:
            # Handle emote commands (including 'stop')
            if message.lower().strip() == "stop":
                await stop_emote(self, user.id)
                await self.highrise.send_whisper(user.id,
                                                 "Emote loop stopped.")
                return
            if await handle_emote_command(self, user, message):
                return
            # Handle other commands
            await handle_command(self, user, message)
        except Exception as e:
            try:
                await self.highrise.send_whisper(
                    user.id, f"Unexpected error processing message: {e}")
            except Exception as e2:
                print(f"Error sending error whisper: {e2}")
            print(f"Chat error: {e}")

    async def run(self, room_id, token):
        try:
            definitions = [BotDefinition(self, room_id, token)]
            await highrise_main(definitions)
        except Exception as e:
            print(f"Error in run: {e}")


class BotDefinition:

    def __init__(self, bot, room_id, api_token):
        self.bot = bot
        self.room_id = room_id
        self.api_token = api_token


if __name__ == "__main__":
    try:
        room_id = os.getenv("HIGHRISE_ROOM_ID", "6871334bd8cf4ac550f0d6f7")
        token = os.getenv(
            "HIGHRISE_API_TOKEN",
            "fda07293a4522efaef4f8e60222a6900c2575f9c05c0336c4c2a77a4502e434a")

        bot = Bot()
        asyncio.run(bot.run(room_id, token))
    except Exception as e:
        print(f"Error starting bot: {e}")
