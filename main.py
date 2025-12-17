from highrise import BaseBot, User, Position, SessionMetadata
from highrise.__main__ import main as highrise_main
import asyncio
import config  # <--- IMPORT 1: Import the whole config module
from config import BOT_ID, ROOM_ID # <--- IMPORT 2: Only import constants here
from event_handlers import on_start, on_reaction, on_user_join, on_tip
from emote_manager import handle_emote_command, stop_emote

# Try to import handle_command, if it doesn't exist, create a dummy function
try:
    from command_handlers import handle_command
except ImportError:
    async def handle_command(bot, user, message):
        pass

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.active_emote_loops = {} 

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        await on_start(self, session_metadata)

    async def on_user_join(self, user: User, position: Position | None = None) -> None:
        await on_user_join(self, user, position)

    async def on_reaction(self, user: User, reaction: str, receiver: User) -> None:
        await on_reaction(self, user, reaction, receiver)

    async def on_tip(self, sender: User, receiver: User, tip: str) -> None:
        await on_tip(self, sender, receiver, tip)

    async def on_message(self, user_id: str, conversation_id: str, is_new_conversation: bool) -> None:
        pass

    async def on_chat(self, user: User, message: str) -> None:
        print(f"[CHAT] {user.username}: {message}")
        try:
            if message.lower().strip() == "stop":
                await stop_emote(self, user.id)
                await self.highrise.send_whisper(user.id, "Emote loop stopped.")
                return

            if await handle_emote_command(self, user, message):
                return

            await handle_command(self, user, message)

        except Exception as e:
            print(f"Chat error: {e}")
            try:
                await self.highrise.send_whisper(user.id, f"Error: {e}")
            except Exception:
                pass

    async def on_user_move(self, user: User, pos: Position) -> None:
        try:
            # Check config.quickteleport so it sees updates (True/False) instantly
            if config.quickteleport:
                await self.highrise.teleport(user.id, pos)
        except Exception as e:
            print(f"User move error: {e}")

    async def run(self, room_id, token):
        definitions = [BotDefinition(self, room_id, token)]
        await highrise_main(definitions)

class BotDefinition:
    def __init__(self, bot, room_id, api_token):
        self.bot = bot
        self.room_id = room_id
        self.api_token = api_token

if __name__ == "__main__":
    try:
        bot = Bot()
        asyncio.run(bot.run(ROOM_ID, BOT_ID))
    except Exception as e:
        print(f"Error starting bot: {e}")