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

highriseroomID = ROOM_ID


# Split long messages into chunks for Highrise limit (max ~300 chars)
def split_message(text, limit=250):
  lines = text.split("\n")
  chunks = []
  current = ""
  for line in lines:
    if len(current) + len(line) + 1 > limit:
      chunks.append(current)
      current = line
    else:
      current += ("\n" if current else "") + line
  if current:
    chunks.append(current)
  return chunks


async def tax(bot, user, message: str):
  try:
    amount_match = re.match(r"[!/]*tax\s+(\d+)", message.lower())
    if not amount_match:
      await bot.highrise.send_whisper(user.id, "⚠️ Usage: !tax <amount>")
      return

    amount = int(amount_match.group(1))

    bars = {
        10000: ("10k bars", 1000),
        5000: ("5k bars", 500),
        1000: ("1k bars", 100),
        500: ("500g bars", 50),
        100: ("100g bars", 10),
        50: ("50g bars", 5),
        10: ("10g bars", 1),
        5: ("5g bars", 1),
        1: ("1g bars", 1)
    }

    breakdown = []
    total = 0
    temp = amount

    for value, (label, fee) in bars.items():
      count = temp // value
      if count > 0:
        taxed = (value + fee) * count
        breakdown.append(
            f"➤ {label:<9}: {value} + {fee} = {value + fee} × {count}")
        total += taxed
        temp -= value * count

    output = f"💸 Tax Calculator 💸\nRequested: {amount}💰\n\nRequired Gold (w/ tax):\n"
    output += "\n".join(breakdown)
    output += f"\n\n🔢 To receive {amount}💰\nYou need to spend: {total}💰 (incl. tax)"

    for part in split_message(output):
      await bot.highrise.send_whisper(user.id, part)
      await asyncio.sleep(0.5)

  except Exception as e:
    await bot.highrise.send_whisper(user.id, f"❌ Error calculating tax: {e}")
    print(f"[Tax Error] {e}")
