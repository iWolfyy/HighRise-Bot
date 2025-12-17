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
from teleport_manager import load_teleports, maketele, save_teleports, teleport_command, delete_teleport, list_teleports
from config import BOT_ID, ROOM_ID, BOT_UID, BOT_START_POSITION, VIP_THRESHOLD

from handlers.help import help
from handlers.other import other
from handlers.mod import mod
from handlers.invite import invite
from handlers.feedback import feedback
from handlers.duets import duets
from handlers.ask import ask
from handlers.reset import reset
from handlers.pos import pos
from handlers.tp import tp
from handlers.summon import summon
from handlers.kick import kick
from handlers.ban import ban
from handlers.mute import mute
from handlers.unban import unban
from handlers.test import test
from handlers.bal import bal
from handlers.tip import tip
from handlers.outfit import handle_equip
from handlers.outfit import handle_unequip
from handlers.outfit import handle_change
from handlers.vip import vip
from handlers.emotes import emotes
from handlers.reactions import heart, heart_all
from handlers.reactions import thumbsup
from handlers.reactions import wave
from handlers.reactions import clap
from handlers.reactions import wink
from handlers.reactions import heart_all
from handlers.givevip import givevip
from handlers.removevip import removevip
from handlers.viplist import viplist
from handlers.movebot import movebot
from handlers.getutils import getutils
from handlers.joke import joke
from handlers.tax import tax
from handlers.news import news
from handlers.quote import quote
from handlers.fact import fact
from handlers.restart import restart
from handlers.manageclothes import purchase_item
from handlers.searchitem import search_item
from reminder_manager import add_reminder
from reminder_manager import list_reminders
from reminder_manager import delete_reminder
from handlers.quicktp import quicktp   

from handlers.punch import punch
tip_lock = asyncio.Lock()

highriseroomID = ROOM_ID


async def handle_command(bot, user: User, message: str) -> None:
    bot_id = BOT_ID
    room_id = ROOM_ID
    _id = f"1_on_1:{bot_id}:{user.id}"
    _idx = f"1_on_1:{user.id}:{bot_id}"

    if message.lower().lstrip().startswith(("!help", "-help")):
        await help(bot, user, message)

    if message.lower().lstrip().startswith(("!other", "-other")):
        await other(bot, user, message)

    if message.lower() == "!mod":
        await mod(bot, user, message)

    if message.lower().lstrip().startswith(("!invite", "-invite")):
        await invite(bot, user, message)

    if message.lower().lstrip().startswith(("!feedback", "-feedback")):
        await feedback(bot, user, message)

    if message.lower().lstrip().startswith(
        ("!fight", "-fight", "!uwu", "-uwu", "!punk", "-punk")):
        await duets(bot, user, message)

    if message.lower().lstrip().startswith(("!ask", "-ask")):
        await ask(bot, user, message)

    if message.lower().lstrip().startswith(("reset", "!reset", "-reset")):
        await reset(bot, user, message)

    if message.lower().lstrip().startswith(("!pos", "-pos")):
        await pos(bot, user, message)

    if message.lower().lstrip().startswith(("!tp", "-tp")):
        await tp(bot, user, message)

    if message.lower().lstrip().startswith(("!summon", "-summon")):
        await summon(bot, user, message)

    if message.lower() == "!heart":
        await heart(bot, user, message)

    if message.lower().lstrip().startswith(("!clap", "-clap")):
        await clap(bot, user, message)

    if message.lower().lstrip().startswith(("!thumbsup", "-thumbsup")):
        await thumbsup(bot, user, message)

    if message.lower().lstrip().startswith(("!wave", "-wave")):
        await wave(bot, user, message)

    if message.lower().lstrip().startswith(("!wink", "-wink")):
        await wink(bot, user, message)

    if message.lower().lstrip().startswith(("!kick", "-kick")):
        await kick(bot, user, message)

    if message.lower().lstrip().startswith(("!ban", "-ban")):
        await ban(bot, user, message)

    if message.lower().lstrip().startswith(("!mute", "-mute")):
        await mute(bot, user, message)

    if message.lower().lstrip().startswith(("!unban", "-unban")):
        await unban(bot, user, message)

    if message.lower().lstrip().startswith(("!test", "-test")):
        await test(bot, user, message)

    if message.lower().lstrip().startswith(("!bal", "-bal")):
        await bal(bot, user, message)

    if message.lower().lstrip().startswith(("!tip", "-tip")):
        await tip(bot, user, message)

    if message.lower().lstrip().startswith(("!vip", "-vip")):
        await vip(bot, user, message)

    if message.lower().strip().startswith("!equip"):
        await handle_equip(bot, user, message)

    if message.lower().strip().startswith("!change"):
        await handle_change(bot, user, message)

    if message.lower().strip().startswith("!unequip"):
        await handle_unequip(bot, user, message)

    if message.lower().lstrip().startswith(("!emotes", "-emotes")):
        await emotes(bot, user, message)

    if message.lower().lstrip().startswith(("!givevip", "-givevip")):
        await givevip(bot, user, message)

    if message.lower().lstrip().startswith(("!removevip", "-removevip")):
        await removevip(bot, user, message)

    if message.lower().startswith("!viplist"):
        await viplist(bot, user, message)

    if message.lower().lstrip().startswith(("!movebot", "-movebot")):
        await movebot(bot, user, message)

    if message.lower().lstrip().startswith(("!maketele", "-maketele")):
        await maketele(bot, user, message)

    await teleport_command(bot, user, message)

    if message.lower().startswith("!teleports"):
        await list_teleports(bot, user)

    elif message.lower().startswith("!deltele"):
        await delete_teleport(bot, user, message)

    if message.lower().lstrip().startswith(("!getutils", "-getutils")):
        await getutils(bot, user, message)

    if message.lower().startswith("!joke"):
        await joke(bot, user, message)

    if message.lower().startswith("!tax"):
        await tax(bot, user, message)

    if message.lower().startswith("!news"):
        await news(bot, user, message)

    if message.lower().startswith("!quote"):
        await quote(bot, user, message)

    if message.lower().startswith("!fact"):
        await fact(bot, user, message)

    if message.lower().startswith("!restart"):
        await restart(bot, user, message)

    if message.lower().startswith("!addreminder"):
        await add_reminder(bot, user, message)

    if message.lower().startswith("!listreminders"):
        await list_reminders(bot, user)

    if message.lower().startswith("!delreminder"):
        await delete_reminder(bot, user, message)

    if message.startswith("!heartall"):
        await heart_all(bot, user, message)

    if message.lower().lstrip().startswith(("!punch", "-punch")):
        await punch(bot, user, message)

    if message.lower().lstrip().startswith(("!quicktp", "-quicktp")):
        await quicktp(bot,user,message)
