import json
import os
import asyncio
from datetime import datetime, timedelta
from utils import find_user
from config import ROOM_ID

REMINDER_FILE = os.path.abspath("reminders.json")
MAX_MESSAGE_LENGTH = 200


def load_reminders():
    """Load reminders from file with data validation"""
    if not os.path.exists(REMINDER_FILE):
        return []

    try:
        with open(REMINDER_FILE, "r") as f:
            data = json.load(f)

            validated_reminders = []
            for r in data:
                if not all(key in r for key in
                           ["id", "interval_min", "next_run", "message"]):
                    continue

                try:
                    r["next_run"] = datetime.fromisoformat(r["next_run"])
                    r["interval_min"] = float(r["interval_min"])
                    validated_reminders.append(r)
                except (ValueError, TypeError):
                    continue

            # Sort by ID to maintain order
            validated_reminders.sort(key=lambda x: x["id"])
            return validated_reminders
    except (json.JSONDecodeError, IOError):
        return []


def save_reminders(data):
    """Save reminders to file with error handling"""
    try:
        # Sort by ID before saving
        data.sort(key=lambda x: x["id"])

        json_data = []
        for r in data:
            r_copy = r.copy()
            r_copy["next_run"] = r["next_run"].isoformat()
            json_data.append(r_copy)

        temp_file = REMINDER_FILE + ".tmp"
        with open(temp_file, "w") as f:
            json.dump(json_data, f, indent=4)

        if os.path.exists(REMINDER_FILE):
            os.remove(REMINDER_FILE)
        os.rename(temp_file, REMINDER_FILE)
    except Exception as e:
        print(f"Error saving reminders: {e}")


def get_next_id(reminders):
    """Get the next sequential ID"""
    if not reminders:
        return 1
    return max(r["id"] for r in reminders) + 1


async def start_reminder_loop(bot):
    while True:
        try:
            reminders = load_reminders()
            now = datetime.now()
            triggered = False

            for reminder in reminders:
                if now >= reminder["next_run"]:
                    try:
                        await bot.highrise.chat(f"{reminder['message']}")

                        interval = timedelta(minutes=reminder["interval_min"])
                        reminder["next_run"] = now + interval
                        triggered = True
                    except Exception as e:
                        print(f"Error sending reminder {reminder['id']}: {e}")

            if triggered:
                save_reminders(reminders)

            sleep_time = await calculate_sleep_time(reminders)
            await asyncio.sleep(sleep_time)

        except Exception as e:
            print(f"[Reminder Loop Error] {e}")
            await asyncio.sleep(5)


async def add_reminder(bot, user, message):
    try:
        parts = message.split()
        if len(parts) < 3:
            await bot.highrise.send_whisper(
                user.id, "Usage: !addreminder minutes message")
            return

        match = await find_user(bot, user.username)
        if not match:
            await bot.highrise.send_whisper(user.id, "User info not found.")
            return

        _, _, _, is_mod, is_owner = match
        if not (is_mod or is_owner):
            await bot.highrise.send_whisper(
                user.id, "❌ Only mods/owner can use this command.")
            return

        try:
            minutes = float(parts[1])
            if minutes <= 0:
                await bot.highrise.send_whisper(user.id,
                                                "❌ Interval must be positive")
                return
            if minutes > 525600:
                await bot.highrise.send_whisper(
                    user.id, "❌ Interval too long (max 1 year)")
                return
        except ValueError:
            await bot.highrise.send_whisper(
                user.id, "❌ Invalid interval (must be a number)")
            return

        reminder_text = " ".join(parts[2:])
        if len(reminder_text) > MAX_MESSAGE_LENGTH:
            await bot.highrise.send_whisper(
                user.id,
                f"❌ Message too long (max {MAX_MESSAGE_LENGTH} chars)")
            return

        reminders = load_reminders()
        reminder_id = get_next_id(reminders)

        new_reminder = {
            "id": reminder_id,
            "interval_min": minutes,
            "next_run": datetime.now() + timedelta(minutes=minutes),
            "message": reminder_text
        }

        reminders.append(new_reminder)
        save_reminders(reminders)

        await bot.highrise.send_whisper(
            user.id,
            f"✅ Reminder added!\n🆔 ID: `{reminder_id}`\n⏱ Every: {minutes} min\n📢 {reminder_text}"
        )

    except Exception as e:
        await bot.highrise.send_whisper(user.id, f"⚠️ Error: {e}")
        print(f"add_reminder error: {e}")


async def list_reminders(bot, user):
    try:
        match = await find_user(bot, user.username)
        if not match:
            await bot.highrise.send_whisper(user.id, "User info not found.")
            return

        _, _, _, is_mod, is_owner = match
        if not (is_mod or is_owner):
            await bot.highrise.send_whisper(
                user.id, "❌ Only mods/owner can use this command.")
            return

        reminders = load_reminders()
        if not reminders:
            await bot.highrise.send_whisper(user.id, "📭 No active reminders.")
            return

        now = datetime.now()
        msg = "**📋 Active Reminders:**\n\n"
        for r in reminders:
            time_left = r["next_run"] - now
            if time_left.total_seconds() <= 0:
                status = "DUE NOW"
            else:
                hours, remainder = divmod(time_left.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                status = f"in {int(hours)}h {int(minutes)}m {int(seconds)}s"

            msg += (f"🆔 `{r['id']}`\n"
                    f"⏰ Every: {r['interval_min']} minutes\n"
                    f"⏳ Next: {status}\n"
                    f"📢 Message: {r['message']}\n\n")

        await bot.highrise.send_whisper(user.id, msg)

    except Exception as e:
        await bot.highrise.send_whisper(user.id, f"⚠️ Error: {e}")
        print(f"list_reminders error: {e}")


async def delete_reminder(bot, user, message):
    try:
        parts = message.split()
        if len(parts) < 2:
            await bot.highrise.send_whisper(user.id, "Usage: !delreminder id")
            return

        try:
            reminder_id = int(parts[1])
        except ValueError:
            await bot.highrise.send_whisper(user.id, "❌ ID must be a number")
            return

        match = await find_user(bot, user.username)
        if not match:
            await bot.highrise.send_whisper(user.id, "User info not found.")
            return

        _, _, _, is_mod, is_owner = match
        if not (is_mod or is_owner):
            await bot.highrise.send_whisper(
                user.id, "❌ Only mods/owner can delete reminders.")
            return

        reminders = load_reminders()
        new_list = [r for r in reminders if r["id"] != reminder_id]

        if len(reminders) == len(new_list):
            await bot.highrise.send_whisper(
                user.id, f"❌ No reminder with ID `{reminder_id}`.")
        else:
            # Renumber all reminders to maintain sequential order
            for index, reminder in enumerate(new_list, start=1):
                reminder["id"] = index

            save_reminders(new_list)
            await bot.highrise.send_whisper(
                user.id,
                f"🗑️ Reminder `{reminder_id}` deleted. IDs renumbered.")

    except Exception as e:
        await bot.highrise.send_whisper(user.id, f"⚠️ Error: {e}")
        print(f"delete_reminder error: {e}")


async def calculate_sleep_time(reminders):
    """Calculate optimal sleep time until next reminder"""
    if not reminders:
        return 60

    now = datetime.now()
    next_run = min(r["next_run"] for r in reminders)
    sleep_seconds = (next_run - now).total_seconds()
    return max(1, min(sleep_seconds, 60))
