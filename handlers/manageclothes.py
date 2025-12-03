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


async def purchase_item(bot, item_id: str) -> bool:
  """
    Purchases an item from the Highrise store using the bot's gold.

    Args:
        item_id (str): The unique ID of the item to purchase.

    Returns:
        bool: True if the purchase was successful, False otherwise.
    """
  try:
    # Check if the item is purchasable via the Web API
    item_data = await bot.webapi.get_item(item_id)
    if not item_data or not getattr(item_data, 'is_purchasable', False):
      print(f"Error: Item {item_id} is not purchasable or does not exist.")
      return False

    # Check if the item is already in the bot's inventory
    inventory = await bot.highrise.get_inventory()
    for item in inventory.items:
      if item.id == item_id:
        print(
            f"Error: Item {item_id} is already in inventory. Bots cannot purchase duplicates."
        )
        return False

    # Attempt to purchase the item
    await bot.highrise.buy_item(item_id)
    print(f"Successfully purchased item {item_id}.")

    # Verify the item was added to inventory
    updated_inventory = await bot.highrise.get_inventory()
    for item in updated_inventory.items:
      if item.id == item_id:
        print(f"Item {item_id} confirmed in inventory.")
        return True

    print(
        f"Error: Item {item_id} purchase succeeded but not found in inventory."
    )
    return False

  except Exception as e:
    print(f"Error purchasing item {item_id}: {str(e)}")
    return False
