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

async def nigga(bot: BaseBot, user: User, message: str) -> None:
    tips_data = load_tips()
    username = user.username.lower()
    user_data = tips_data.get(username, {"amount": 0, "vip": False})
    amount = user_data["amount"]
    is_vip = user_data["vip"]
    if is_vip:

    else:
