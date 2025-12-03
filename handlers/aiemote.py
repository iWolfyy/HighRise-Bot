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
from config import BOT_ID, ROOM_ID, BOT_UID, BOT_START_POSITION, VIP_THRESHOLD, HF_API_KEY

emote_keywords = {
    "happy": [
        "yay", "yayy", "yey", "yeet", "good", "great", "awesome", "fun", "lol",
        "haha", "heh", "nice", "cool", "pog", "dope", "vibe", "vibing", "lit",
        "cheer", "cheered", "ez", "clapped", "funny", "goofy", "yayyy", "yess",
        "omg yes", "purr", "winning", "up", "blessed", "valid", "noice",
        "slay", "goat", "on top", "golden", "smooth", "loving it", "laughing",
        "happy tears", "smiles", "lolol", "lmao", "laughs", "crackin up",
        "bursting", "rofl", "good vibes", "sunshine", "bright", "glowin",
        "vibes immaculate", "pure joy"
    ],
    "angry": [
        "angry", "mad", "annoyed", "rage", "raging", "bruh", "wtf", "trash",
        "bs", "lame", "stupid", "idiot", "dumb", "noob", "pissed", "fuming",
        "furious", "tilted", "frustrated", "brooo", "nahhh", "over it",
        "im done", "hell nah", "raged", "lost it", "trash af", "mid", "loser",
        "angery", "i hate this", "wtfff", "sucks", "smh", "furious af",
        "not again", "nah bro", "this dumb", "why me", "stop it", "bro what",
        "that’s wild", "done with this"
    ],
    "sad": [
        "sad", "cry", "crying", "cried", "tears", "😭", "broken", "break",
        "heartbroken", "lonely", "pain", "hurt", "depressed", "miss",
        "missing", "rip", "dead inside", "blue", "emo", "down bad", "so alone",
        "ache", "achey", "hollow", "grief", "omg no", "nooo", "devastated",
        "shattered", "low", "hurtin", "drained", "exhausted", "in pain",
        "gone", "ruined", "lost", "abandoned", "helpless", "hopeless",
        "gloomy", "tearful", "sobbing", "bawling", "shaking", "cryfest",
        "emotional wreck", "done for", "wounded", "melancholy"
    ],
    "love": [
        "love", "cute", "cutie", "adorable", "hot", "bae", "babe", "baby",
        "bby", "crush", "mwah", "xoxo", "sweet", "beautiful", "pretty",
        "gorgeous", "stunning", "❤️", "💕", "😍", "angel", "boo", "soulmate",
        "ily", "in love", "hubby", "wifey", "blushing", "rosy", "snuggle",
        "cuddle", "kiss", "hug", "dear", "snuggles", "cuteness overload",
        "ur everything", "honey", "sugar", "pumpkin", "lovebirds", "romantic",
        "loved up", "smitten", "i adore u", "ur mine", "always yours",
        "forever bae", "love u tons", "ur my heart", "babycakes", "ur perfect"
    ],
    "confused": [
        "what", "huh", "why", "bruh what", "tf", "wtf", "idk", "no clue",
        "confused", "lost", "dumbfounded", "hmm", "unsure", "puzzled", "eh",
        "ain’t no way", "explain", "say what", "cap?", "wait huh", "um",
        "u sure?", "fr?", "bruhhhh", "man what", "helppp", "how come", "sus",
        "make it make sense", "wt heck", "yo wut", "nah that’s weird",
        "question marks", "blanking", "doesn’t add up", "overthinking",
        "overload", "overstimulated", "headache"
    ],
    "excited": [
        "excited", "hyped", "hyper", "energized", "let's go", "finally", "yes",
        "yessir", "omg", "yay", "party", "buzzing", "cheerful", "lit",
        "poppin", "amped", "fired up", "upbeat", "glowing", "pumped",
        "on fire", "bouncing", "crazy hype", "zooming", "full energy",
        "boosted", "highkey", "vibe check passed", "beyond ready", "ready af",
        "can't wait", "jumping", "too hype", "running wild", "shining",
        "beaming", "tingling", "rush", "lit af"
    ],
    "bored": [
        "bored", "tired", "sleepy", "sleep", "zzz", "snooze", "slow", "meh",
        "dry", "dragging", "lazy", "chillin", "snore", "yawn", "nothing to do",
        "same old", "looping", "ugh", "dull", "idle", "burned out", "tired af",
        "boredom", "stale", "blank", "slow day", "dead inside", "lifeless",
        "void", "i’m melting", "slow motion", "numb", "low energy",
        "checked out"
    ],
    "scared": [
        "scared", "afraid", "fear", "panic", "nervous", "shiver", "goosebumps",
        "anxious", "paranoid", "spooked", "creeped out", "shook", "frightened",
        "terrified", "pls no", "ghost", "jump scare", "eerie",
        "bro i’m scared", "screaming", "😨", "nah fam", "haunted",
        "wtf was that", "yikes", "worried", "freaked", "buggin", "hold me",
        "dark vibes", "chills", "shuddering", "dreading", "wtf is this",
        "mommy help", "uh oh", "run", "hide"
    ],
    "motivated": [
        "grind", "hustle", "winning", "focus", "boss", "success", "conquer",
        "dominate", "rise", "push", "you got this", "believe", "dream",
        "no sleep", "dedicated", "goal", "let’s gooo", "unstoppable",
        "mindset", "get it", "next level", "alpha", "vision",
        "built different", "move in silence", "let’s grind", "work mode",
        "locked in", "elevated", "all gas no brakes", "power move", "ascend",
        "beast mode", "discipline", "driven", "no distractions",
        "tunnel vision"
    ],
    "flirty": [
        "flirty", "wink", "tease", "😉", "sugar", "hey baby", "you single",
        "bae", "hot stuff", "you fine", "rizz", "ur cute", "hey gorgeous",
        "snack", "ur hot", "you mine", "damn", "blushin", "slide in", "👀",
        "eyyy", "what u doin", "smooth talker", "lover boy", "mamacita",
        "cutiepie", "hey handsome", "dreamy", "hey there 😉", "kissy",
        "damn okay", "babe alert", "dayumm", "flamin", "heart eyes",
        "pick me vibes", "u got rizz", "smooth operator"
    ],
    "sassy": [
        "girl bye", "uh huh", "okayyy", "whatever", "don’t", "stop it",
        "excuse me", "boo hoo", "talk to the hand", "okay diva", "get over it",
        "ugh please", "as if", "that’s wild", "mmm hmm", "who asked",
        "nah not today", "chill", "sit down", "eat it", "sip tea",
        "bye felicia", "🧍‍♀️", "no ma'am", "louder", "say it again",
        "not impressed", "and what?", "bless your heart", "bffr",
        "miss me with that", "delulu", "perrrr", "real bad", "petty queen"
    ],
    "mischievous": [
        "hehe", "gotcha", "troll", "sneaky", "plotting", "scheming",
        "evil laugh", "mischief", "prank", "whoops", "uh oh", "busted",
        "ehehe", "bamboozled", "you fell for it", "oopsie", "trick", "messin",
        "chaotic", "evil plan", "hehehe", "devilish", "villain", "maniacal",
        "lulz", "joker mode", "up to no good", "devious", "pullin strings",
        "playing dumb", "diabolical", "planned it all", "who, me?",
        "caught in 4k", "nahh trust me", "sneak lvl 100"
    ]
}

emote_actions = {
    "happy": [
        "emote-happy", "emoji-clapping", "dance-tiktok8", "emote-peace",
        "emoji-celebrate", "dance-smoothwalk", "dance-robotic"
    ],
    "angry":
    "emote-charging",
    "sad":
    "emote-sad",
    "love":
    "emote-kiss",
    "confused":
    "idle-uwu",
    "excited":
    "emote-punkguitar",
    "bored":
    "emote-fail1",
    "scared":
    "emote-embarrassed",
    "motivated":
    "emote-kicking",
    "flirty":
    "emote-deathdrop",
    "sassy":
    "idle_singing",
    "mischievous":
    "emoji-naughty"
}


def detect_emote(text: str) -> str:
    text = text.lower()
    for emotion, keywords in emote_keywords.items():
        for keyword in keywords:
            if keyword in text:
                action = emote_actions[emotion]
                if isinstance(action, list):
                    return random.choice(action)
                return action
    return None


async def auto_emote(bot, text: str):
    emote = detect_emote(text)
    if emote:
        try:
            await asyncio.sleep(1)
            await bot.highrise.send_emote(emote, BOT_UID)
        except Exception as e:
            print(f"[emote fail] {e}")
