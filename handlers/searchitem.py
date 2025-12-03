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


async def search_item(bot: BaseBot, user: User, message: str) -> None:
    """
    Handles the !searchitem command to search for an item by name and return its item ID.
    Includes try-except blocks to catch and log errors at each step.

    Args:
        bot: The bot instance.
        user: The user issuing the command.
        message: The full command message (e.g., "!searchitem denim jacket [index]").
    """
    try:
        # Step 1: Parse the message
        try:
            parts = message.strip().split()
            if len(parts) < 2:
                await bot.highrise.send_whisper(
                    user.id, "Usage: !searchitem <item_name> [index]")
                return
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error parsing command: {str(e)}")
            print(f"[PARSE ERROR] Failed to split message '{message}': {e}")
            return

        # Step 2: Extract item name and index
        try:
            item_name = " ".join(
                parts[1:-1]) if parts[-1].isdigit() else " ".join(parts[1:])
            index = int(parts[-1]) if parts[-1].isdigit() else 0
            item_name_normalized = item_name.lower().strip()
            print(
                f"[DEBUG] Parsed item_name: '{item_name}', normalized: '{item_name_normalized}', index: {index}"
            )
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error extracting item name or index: {str(e)}")
            print(
                f"[EXTRACT ERROR] Failed to process item name or index from '{message}': {e}"
            )
            return

        # Step 3: Fetch items from Web API
        try:
            items = (await bot.webapi.get_items(item_name=item_name_normalized
                                                )).items
            print(
                f"[DEBUG] API response for '{item_name_normalized}': {len(items)} items found"
            )
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error fetching items from API: {str(e)}")
            print(
                f"[API ERROR] Failed to call get_items for '{item_name_normalized}': {e}"
            )
            return

        # Step 4: Check if items were found
        try:
            if not items:
                await bot.highrise.send_whisper(
                    user.id,
                    f"No items found for '{item_name}'. Try checking the exact name or use lowercase."
                )
                await bot.highrise.send_whisper(
                    user.id,
                    "If this is a grab or event item, it may not be in the standard item database."
                )
                print(f"[DEBUG] No items found for '{item_name_normalized}'")
                return
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error checking item results: {str(e)}")
            print(f"[CHECK ITEMS ERROR] Failed to verify items list: {e}")
            return

        # Step 5: Validate index
        try:
            if index >= len(items):
                await bot.highrise.send_whisper(
                    user.id,
                    f"Invalid index {index}. Found {len(items)} items.")
                print(f"[DEBUG] Invalid index {index} for {len(items)} items")
                return
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error validating index: {str(e)}")
            print(f"[INDEX ERROR] Failed to validate index {index}: {e}")
            return

        # Step 6: Select and process the item
        try:
            item = items[index]
            item_id = item.item_id
            item_name_found = item.item_name
            print(
                f"[DEBUG] Selected item: {item_name_found} ({item_id}) at index {index}"
            )
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error accessing item at index {index}: {str(e)}")
            print(
                f"[ITEM ACCESS ERROR] Failed to access item at index {index}: {e}"
            )
            return

        # Step 7: Provide feedback based on number of matches
        try:
            if len(items) > 1:
                await bot.highrise.send_whisper(
                    user.id,
                    f"Found {len(items)} items for '{item_name}'. Using item {index}: {item_name_found} ({item_id})."
                )
            else:
                await bot.highrise.send_whisper(
                    user.id, f"Found item: {item_name_found} ({item_id}).")
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error sending item feedback: {str(e)}")
            print(f"[FEEDBACK ERROR] Failed to send item feedback: {e}")
            return
        try:
            await bot.highrise.send_whisper(user.id, f"Item ID: {item_id}")
            print(f"[DEBUG] Successfully returned item ID: {item_id}")
        except Exception as e:
            await bot.highrise.send_whisper(
                user.id, f"Error sending item ID: {str(e)}")
            print(f"[SEND ID ERROR] Failed to send item ID '{item_id}': {e}")
            return

    except Exception as e:
        await bot.highrise.send_whisper(
            user.id, f"Unexpected error searching for '{item_name}': {str(e)}")
        print(
            f"[GENERAL ERROR] Unexpected error in handle_search_item_command: {e}"
        )
