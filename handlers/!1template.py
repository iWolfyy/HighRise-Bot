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


  💎 ULTIMATE HIGHRISE BOT 💎
  By @Mr_Wolfy

  ✨ Features:
  🎭 Emote Functions

  🛡️ Mod Controls (Kick/Ban/Mute)

  💬 Auto Welcome Messages

  ⚡ Teleport System

  💵 VIP Access

  🧠 AI Features

  💸 Tipping Functions

  🗺️ Add / Delete Custom Teleports

  🖼️ Change Bot Avatar & Outfit

  🔐 Role-Based Access (Owner / Mod / VIP)

  🛠️ Custom Features (On Request)

  🔥 Detailed Commands:
  Moderator Commands:

  !kick @user — Kick a user

  !ban @user — Ban a user

  !mute @user — Mute a user

  !unban @user — Unban a user

  !test @user — Check user privileges

  Teleport Commands:

  !tp @user — Teleport to a user

  !pos @user — Get user position

  !summon @user — Summon user to your position

  reset — Respawn at default position

  !maketele [name] [roles...] — Create teleport spot

  !deltele [name] — Delete teleport spot

  !teleports — List teleport spots

  VIP System:

  !givevip @user — Grant VIP (Owner only)

  !removevip @user — Remove VIP (Owner only)

  !vip — Check your VIP status

  !viplist — List all VIPs

  Tipping Functions:

  !tip <amount> — Tip gold to all

  !bal — Show bot gold balance

  !tax <amount> — Highrise Gold Tax Calculator

  AI & Chat:

  !ask [question] — Ask the bot anything

  Fun & Info:

  !joke — Get random jokes

  !tax — Highrise Gold Tax Calculator

  !news — Top news of the day

  !fact — Get random facts

  Bot Appearance:

  Change Bot Avatar & Outfit:

  !Equip - Equip an item on the bot's outfit.

  !Unequip - Remove items of a specified category from the bot's outfit.

  !Change - Change Bot's Outfit Color.

  💰 Pricing:
  Plan	Price	Description
  🔹 1 Day	300 Gold	Test the bot with full features.
  🔸 1 Month	4,500 Gold	Full access, perfect for events.
  💎 Lifetime	13,000 Gold	Own the bot forever with full features.

  🚀 Why Choose Us?
  24/7 Uptime: Always online, never missing a beat.

  Easy to Use: Simple commands, instant results.

  Customizable: Tailor-made features to fit your room’s vibe.

  Support: Direct help from @Mr_Wolfy anytime.

  📩 How to Buy
  DM @Mr_Wolfy now to get your hands on the Ultimate Highrise Bot!

  🔗 More Info & Demo
  Contact @Mr_Wolfy for FAQs or join my room through the bio in my profile for a live demo of the bot.

  📣 Don’t miss out — upgrade your Highrise room today with the smartest, fastest, and most reliable bot around!

  #buy #sell #explore #sf #bot #robot #buying #selling