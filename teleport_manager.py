import json
import os
import asyncio
from highrise import BaseBot, User, Position
from utils import find_user
from tip_manager import load_tips
from config import ROOM_ID

TELEPORTS_FILE = "teleports.json"


# ✅ Load Telepors
def load_teleports():
    if os.path.exists(TELEPORTS_FILE):
        with open(TELEPORTS_FILE, "r") as f:
            return json.load(f)
    return {}


# ✅ Save all the teleports
def save_teleports(data):
    with open(TELEPORTS_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ✅ List all teleport names and roles
async def list_teleports(bot, user):
    teleports = load_teleports()
    if not teleports:
        await bot.highrise.send_whisper(user.id,
                                        "📭 No custom teleports found.")
        return

    msg = "📍 **Custom Teleports**\n\n"
    for name, data in teleports.items():
        roles = data.get("roles", [])
        if not roles:
            role_display = "🌐 Everyone"
        else:
            # Use emojis for roles
            role_display = []
            for role in roles:
                if role == "owner":
                    role_display.append("👑 Owner")
                elif role == "mod":
                    role_display.append("🛡️ Mod")
                elif role == "vip":
                    role_display.append("💎 VIP")
            role_display = ", ".join(role_display)

        msg += f"🔹 **{name}** — {role_display}\n"

    await bot.highrise.send_whisper(user.id, msg)


# ✅ Make a Teleport
async def maketele(bot: BaseBot, user: User, message: str):
    try:
        parts = message.split()
        if len(parts) < 2:
            await bot.highrise.send_whisper(
                user.id, "Usage: !maketele <name> [roles...]")
            return

        teleport_name = parts[1].lower()
        allowed_roles = [r.lower() for r in parts[2:]]  # optional roles

        # Check permissions of user who tries to make teleport
        match = await find_user(bot, user.username)
        if not match:
            await bot.highrise.send_whisper(user.id, "User info not found.")
            return

        _, _, is_vip, is_mod, is_owner = match

        if not (is_owner or is_mod):
            await bot.highrise.send_whisper(
                user.id,
                "You need to be a moderator or owner to create teleports.")
            return

        # Get current user position
        _, user_pos, _, _, _ = match
        if not user_pos:
            await bot.highrise.send_whisper(user.id,
                                            "Could not get your position.")
            return

        # Save teleport info
        teleports = load_teleports()
        teleports[teleport_name] = {
            "position": {
                "x": user_pos.x,
                "y": user_pos.y,
                "z": user_pos.z,
                "facing": user_pos.facing or "FrontLeft"
            },
            "roles": allowed_roles
        }
        save_teleports(teleports)

        roles_text = ", ".join(allowed_roles) if allowed_roles else "everyone"
        await bot.highrise.send_whisper(
            user.id,
            f"Teleport '{teleport_name}' created! Allowed roles: {roles_text}")

    except Exception as e:
        await bot.highrise.send_whisper(user.id,
                                        f"Error creating teleport: {e}")
        print(f"maketele error: {e}")


# ✅ Teleport the User
async def teleport_command(bot: BaseBot, user: User, message: str):
    try:
        command = message.lstrip("!").strip().lower()
        teleports = load_teleports()

        if command not in teleports:
            return  # Not a custom teleport command

        # Get user roles
        match = await find_user(bot, user.username)
        if not match:
            await bot.highrise.send_whisper(user.id, "User info not found.")
            return

        _, _, is_vip, is_mod, is_owner = match

        # Role checking
        allowed_roles = teleports[command].get("roles", [])
        if allowed_roles:
            has_access = False
            for role in allowed_roles:
                if role == "owner" and is_owner:
                    has_access = True
                elif role == "mod" and (is_mod or
                                        is_owner):  # Owners get mod access too
                    has_access = True
                elif role == "vip" and (is_vip or is_mod or is_owner
                                        ):  # Mods & owners get vip access too
                    has_access = True

            if not has_access:
                await bot.highrise.send_whisper(
                    user.id, "🚫 You don't have access to that teleport.")
                return

        # Teleport the user
        pos_data = teleports[command]["position"]
        position = Position(x=pos_data["x"],
                            y=pos_data["y"],
                            z=pos_data["z"],
                            facing=pos_data.get("facing", "FrontLeft"))

        await bot.highrise.teleport(user.id, position)
        await bot.highrise.send_whisper(user.id,
                                        f"✅ Teleported to `{command}`.")

    except Exception as e:
        await bot.highrise.send_whisper(user.id, f"⚠️ Teleport error: {e}")
        print(f"teleport_command error: {e}")


# ✅ Delete a teleport (mods/owners only)
async def delete_teleport(bot, user, message):
    parts = message.split()
    if len(parts) < 2:
        await bot.highrise.send_whisper(user.id, "Usage: !deltele <name>")
        await list_teleports(bot, user)
        return

    from utils import find_user
    match = await find_user(bot, user.username)
    if not match:
        await bot.highrise.send_whisper(user.id, "User info not found.")
        return

    _, _, is_vip, is_mod, is_owner = match
    if not (is_mod or is_owner):
        await bot.highrise.send_whisper(
            user.id, "❌ You don't have permission to delete teleports.")
        return

    name = parts[1].lower()
    teleports = load_teleports()

    if name not in teleports:
        await bot.highrise.send_whisper(user.id,
                                        f"❌ Teleport `{name}` not found.")
        return

    del teleports[name]
    save_teleports(teleports)
    await bot.highrise.send_whisper(user.id, f"✅ Teleport `{name}` deleted.")
