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
import random
from utils import find_user
from tip_manager import load_tips, add_tip, give_vip, remove_vip
from config import BOT_ID, ROOM_ID, BOT_UID, BOT_START_POSITION, VIP_THRESHOLD

highriseroomID = ROOM_ID


async def joke(bot, user, message: str):
  laughing_msgs = [
      "😂😂😂", "🤣🤣🤣", "😆😆😆", "😹😹😹", "😄😄😄", "😝😝😝", "😂🤣😆", "😜😜😜", "😁😁😁", "😛😛😛"
  ]
  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(
          "https://official-joke-api.appspot.com/random_joke") as resp:
        if resp.status != 200:
          await bot.highrise.send_whisper(
              user.id, "Sorry, couldn't fetch a joke right now.")
          return
        data = await resp.json()
        setup = data.get("setup", "")
        punchline = data.get("punchline", "")
        await bot.highrise.chat(setup)
        await asyncio.sleep(1.8)
        await bot.highrise.chat(punchline)
        await asyncio.sleep(0.5)
        laugh_msg = random.choice(laughing_msgs)
        await bot.highrise.chat(laugh_msg)
  except Exception as e:
    await bot.highrise.send_whisper(user.id, f"Error fetching joke: {e}")
    print(f"Joke command error: {e}")
