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


async def periodic_message(bot):
    while True:
        await bot.highrise.chat("This is a periodic message.")
        await asyncio.sleep(2)  # every 30 mins
