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

tip_lock = asyncio.Lock()

highriseroomID = ROOM_ID


async def handle_equip(bot: BaseBot, user: User, message: str) -> None:
    """
    Handles the !equip command to equip an item on the bot's outfit.
    
    Args:
        bot: The bot instance.
        user: The user issuing the command.
        message: The full command message (e.g., "!equip item_name [index]").
    """
    try:
        parts = message.split(" ")
        if len(parts) < 2:
            await bot.highrise.chat("You need to specify the item name.")
            return
        item_name = " ".join(parts[1:-1]) if parts[-1].isdigit() else " ".join(
            parts[1:])
        index = int(parts[-1]) if parts[-1].isdigit() else 0
        item = (await bot.webapi.get_items(item_name=item_name)).items
        if not item:
            await bot.highrise.chat(f"Item '{item_name}' not found.")
            return
        elif len(item) > 1:
            await bot.highrise.chat(
                f"Multiple items found for '{item_name}', using the item number {index} in the list {item[index].item_name}."
            )
        item = item[index]
        item_id = item.item_id
        category = item.category
        verification = False
        inventory = (await bot.highrise.get_inventory()).items
        try:
            await bot.highrise.buy_item(item_id)

        except Exception as e:
            print(f"[EQUIP ERROR] {e}")
            await bot.highrise.send_whisper(user.id,
                                            f"Error during equip: {e}")
        new_item = Item(
            type="clothing",
            amount=1,
            id=item_id,
            account_bound=False,
            active_palette=0,
        )
        outfit = (await bot.highrise.get_my_outfit()).outfit
        items_to_remove = []
        for outfit_item in outfit:
            item_category = outfit_item.id.split("-")[0][0:4]
            print(f"Item category: {item_category}")
            if item_category == category[0:4]:
                items_to_remove.append(outfit_item)
        for item_to_remove in items_to_remove:
            outfit.remove(item_to_remove)
        if category == "hair_front":
            hair_back_id = item.link_ids[0]
            hair_back = Item(
                type="clothing",
                amount=1,
                id=hair_back_id,
                account_bound=False,
                active_palette=0,
            )
            outfit.append(hair_back)
        outfit.append(new_item)
        await bot.highrise.set_outfit(outfit)
        await bot.highrise.send_whisper(
            user.id, f"Equipped item '{item_name}' successfully.")
    except Exception as e:
        await bot.highrise.send_whisper(user.id, f"Error during equip: {e}")
        print(f"[EQUIP ERROR] {e}")


async def handle_unequip(bot: BaseBot, user: User, message: str) -> None:
    """
    Handles the !unequip command to remove items of a specified category from the bot's outfit.
    
    Args:
        bot: The bot instance.
        user: The user issuing the command.
        message: The full command message (e.g., "!unequip category").
    """
    categories = [
        "aura", "bag", "blsh", "body", "dress", "earings", "emote", "eye",
        "eyebrow", "fishing_rod", "freckle", "fullsuit", "glasses", "gloves",
        "hair", "hair_front", "handbag", "hat", "jacket", "lashes", "mole",
        "mouth", "necklace", "nose", "rod", "shirt", "shoes", "shorts",
        "skirt", "sock", "tattoo", "watch"
    ]
    try:
        parts = message.strip().split()
        if len(parts) != 2:
            await bot.highrise.send_whisper(user.id,
                                            "Usage: !unequip <category>")
            await bot.highrise.send_whisper(
                user.id,
                "aura bag blsh body dress earings emote eye eyebrow fishing_rod "
            )
            await bot.highrise.send_whisper(
                user.id,
                "freckle fullsuit glasses gloves hair hair_front handbag hat jacket lashes"
            )
            await bot.highrise.send_whisper(
                user.id,
                "mole mouth necklace nose rod shirt shoes shorts skirt sock tattoo watch"
            )
            return
        input_category = parts[1].lower()
        if input_category not in categories:
            await bot.highrise.send_whisper(
                user.id, f"Invalid category: '{input_category}'.")
            await bot.highrise.send_whisper(
                user.id,
                "aura bag blsh body dress earings emote eye eyebrow fishing_rod "
            )
            await bot.highrise.send_whisper(
                user.id,
                "freckle fullsuit glasses gloves hair hair_front handbag hat jacket lashes"
            )
            await bot.highrise.send_whisper(
                user.id,
                "mole mouth necklace nose rod shirt shoes shorts skirt sock tattoo watch"
            )
            return
            return
        outfit = (await bot.highrise.get_my_outfit()).outfit
        filtered_outfit = []
        removed_any = False
        for item in outfit:
            try:
                item_category = item.id.split("-")[0][0:4]
                if item_category != input_category[0:4]:
                    filtered_outfit.append(item)
                else:
                    removed_any = True
            except Exception as e:
                print(f"Error parsing item id {item.id}: {e}")
                filtered_outfit.append(item)
        if not removed_any:
            await bot.highrise.send_whisper(
                user.id,
                f"No items from category '{input_category}' were equipped.")
            return
        await bot.highrise.set_outfit(filtered_outfit)
        await bot.highrise.send_whisper(
            user.id, f"Removed all '{input_category}' items from outfit.")
    except Exception as e:
        await bot.highrise.send_whisper(user.id, f"Error during unequip: {e}")
        print(f"[UNEQUIP ERROR] {e}")


async def handle_change(bot: BaseBot, user: User, message: str) -> None:
    """
    Handles the !change command to change the color palette of an equipped item.
    
    Args:
        bot: The bot instance.
        user: The user issuing the command.
        message: The full command message (e.g., "!change category color_palette").
    """
    try:
        parts = message.split(" ")
        if len(parts) != 3:
            await bot.highrise.chat(
                "Invalid command format. You need to specify the category and color palette number."
            )
            await bot.highrise.chat(
                "blush , body , hair_front , hair_back , eye , face_hair , mouth"
            )
            return
        category = parts[1]
        try:
            color_palette = int(parts[2])
        except:
            await bot.highrise.chat(
                "Invalid command format. You need to specify the category and color palette number."
            )
            return
        outfit = (await bot.highrise.get_my_outfit()).outfit
        for outfit_item in outfit:
            item_category = outfit_item.id.split("-")[0]
            if item_category == category:
                try:
                    outfit_item.active_palette = color_palette
                except:
                    await bot.highrise.chat(
                        f"The bot isn't using any item from the category '{category}'."
                    )
                    return
        await bot.highrise.set_outfit(outfit)
        await bot.highrise.send_whisper(
            user.id,
            f"Changed color palette of '{category}' to {color_palette}.")
    except Exception as e:
        await bot.highrise.send_whisper(user.id, f"Error during change: {e}")
        print(f"[CHANGE ERROR] {e}")
