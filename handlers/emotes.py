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

async def emotes(bot: BaseBot, user: User, message: str) -> None:
    try:
        words = [
            "rest", "zombie", "relaxed", "attentive", "sleepy",
            "pouty_face", "posh", "tired", "taploop", "sit", "shy",
            "bummed", "chillin", "annoyed", "aerobics", "ponder",
            "hero_pose", "relaxing", "cozy_nap", "enthused",
            "boogie_swing", "feel_the_beat", "irritated", "yes",
            "i_believe_i_can_fly", "the_wave", "think", "theatrical",
            "tapdance", "superrun", "superpunch", "sumofight", "thumbsuck",
            "splitsdrop", "snowballfight", "snowangel", "handshake", "sad",
            "pull", "roll", "rofl", "robot", "rainbow", "proposing",
            "peekaboo", "peace", "panic", "no", "ninjarun", "nightfever",
            "monsterfail", "model", "flirtywave", "levelup", "amused",
            "laugh", "kiss", "superkick", "jump", "judochop", "jetpack",
            "hugyourself", "sweating", "heroentrance", "hello", "headball",
            "harlemshake", "happy", "handstand", "greedyemote", "graceful",
            "moonwalk", "ghostfloat", "gangnamstyle", "frolic", "faint",
            "clumsy", "fall", "face_palm", "exasperated", "elbowbump",
            "disco", "blastoff", "faintdrop", "collapse", "revival", "dab",
            "curtsy", "confusion", "cold", "charging", "bunnyhop", "bow",
            "boo", "homerun", "fallingapart", "thumbsup", "point",
            "sneeze", "smirk", "sick", "gasp", "punch", "pray", "stinky",
            "naughty", "mindblown", "lying", "levitate", "fireballlunge",
            "giveup", "tummy_ache", "flex", "stunned", "cursing_emote",
            "sob", "clap", "raisetheroof", "arrogance", "angry",
            "voguehands", "savagedance", "dontstartnow", "yogaflow",
            "smoothwalk", "ringonit", "letsgoshopping", "russian",
            "robotic", "pennywise", "orangejuicedance", "rockout",
            "karate", "macarena", "hands_in_the_air", "floss", "duckwalk",
            "breakdance", "kpopdance", "pushups", "hyped", "jinglebell",
            "nervous", "toilet", "attention", "astronaut", "dancezombie",
            "ghost", "hearteyes", "swordfight", "timejump", "snake",
            "heartfingers", "heartshape", "hug", "eyeroll", "embarrassed",
            "float", "telekinesis", "sexydance", "puppet", "fighteridle",
            "penguindance", "creepypuppet", "sleigh", "maniac",
            "energyball", "singing", "frog", "superpose", "cute",
            "tiktokdance9", "weirddance", "tiktokdance10", "pose7",
            "pose8", "casualdance", "pose1", "pose3", "pose5", "cutey",
            "punkguitar", "zombierun", "fashionista", "gravity",
            "icecreamdance", "wrongdance", "uwu", "tiktokdance4",
            "advancedshy", "anime_dance", "kawaii", "scritchy",
            "iceskating", "surprisebig", "celebrationstep", "creepycute",
            "frustrated", "pose10", "repose", "tiktok7", "shrink",
            "ditzypose", "teleporting", "touch", "airguitar",
            "thisisforyou", "pushit", "sweetsmooch", "tiktok11",
            "cutesalute", "salut"
        ]
        chunk_size = 10
        for i in range(0, len(words), chunk_size):
            chunk = words[i:i + chunk_size]
            message = ", ".join(chunk)
            await bot.highrise.send_whisper(user.id, message)
            await asyncio.sleep(0.3)
    except Exception as e:
        await bot.highrise.send_whisper(user.id,
                                        f"Error Showing Emotes: {e}")
        print(f"Error Showing Emotes: {e}")
    return