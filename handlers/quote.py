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

tip_lock = asyncio.Lock()

highriseroomID = ROOM_ID


async def quote(bot, user, message: str):
  url = "https://api.quotable.io/random"
  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as resp:
        if resp.status != 200:
          await bot.highrise.send_whisper(
              user.id, "⚠️ Couldn't fetch a quote right now. Try again later.")
          return
        data = await resp.json()
        content = data.get("content", "No quote found.")
        author = data.get("author", "Unknown")
        reply = f"💡 \"{content}\" — *{author}*"
        await bot.highrise.send_whisper(user.id, reply)
  except Exception as e:
    await bot.highrise.send_whisper(user.id, f"❌ Error fetching quote: {e}")
    print(f"[Quote command error] {e}")
