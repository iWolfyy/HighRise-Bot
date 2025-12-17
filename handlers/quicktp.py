import config  # Import the whole module to access variables
import re      # Import regex to modify the text file
from highrise import BaseBot, User

async def quicktp(bot: BaseBot, user: User, message: str) -> None:
    # 1. Check Permissions
    try:
        room = await bot.webapi.get_room(config.ROOM_ID)
        ownerID = room.room.owner_id
        room_priv = await bot.highrise.get_room_privilege(user.id)

        # Allow if user is Moderator OR the Room Owner
        if not room_priv.moderator and ownerID != user.id:
            await bot.highrise.send_whisper(user.id, "You need moderator privileges to use !quicktp.")
            return
    except Exception as e:
        print(f"Quicktp privilege check error: {e}")
        return

    # 2. Toggle and Save to File
    try:
        # Get current state from memory
        current_state = config.quickteleport
        new_state = not current_state # Flip True/False

        # A. Update In-Memory Variable (Immediate effect)
        config.quickteleport = new_state

        # B. Update the config.py File (Permanent save)
        try:
            with open("config.py", "r") as f:
                content = f.read()

            # Regex to find "quickteleport = True/False" and replace it
            new_content = re.sub(
                r"quickteleport\s*=\s*(True|False)", 
                f"quickteleport = {new_state}", 
                content
            )

            with open("config.py", "w") as f:
                f.write(new_content)

            status_str = "ON" if new_state else "OFF"
            await bot.highrise.send_whisper(user.id, f"Quick Teleport is now {status_str}.")

        except Exception as file_error:
            print(f"Error writing to config.py: {file_error}")
            await bot.highrise.send_whisper(user.id, "Setting changed in memory, but failed to save to file.")

    except Exception as e:
        await bot.highrise.send_whisper(user.id, f"Error toggling quicktp: {e}")
        print(f"Error quickteleport: {e}")