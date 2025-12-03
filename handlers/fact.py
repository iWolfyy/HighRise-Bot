from highrise import *
from highrise.webapi import *
from highrise.models_webapi import *
from highrise.models import *
from highrise.models import Item
import asyncio
import requests
import random
import re
import aiohttp
from utils import find_user
from tip_manager import load_tips, add_tip, give_vip, remove_vip
from config import BOT_ID, ROOM_ID, BOT_UID, BOT_START_POSITION, VIP_THRESHOLD

highriseroomID = ROOM_ID


async def fact(bot, user, message: str):
  url = "https://uselessfacts.jsph.pl/random.json?language=en"
  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as resp:
        if resp.status != 200:
          await bot.highrise.send_whisper(
              user.id, "⚠️ Couldn't fetch a fact right now.")
          return
        data = await resp.json()
        fact_text = data.get("text", "No fact found.")
        await bot.highrise.chat(f"💡 Fact: {fact_text}")
  except Exception as e:
    await bot.highrise.send_whisper(user.id, f"❌ Error fetching fact: {e}")
    print(f"Fact command error: {e}")
