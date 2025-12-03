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
from handlers.aiemote import auto_emote

API_URL = "https://router.huggingface.co/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
}
helpurl = "https://highrisebotinfo.vercel.app/"
helpresponse = requests.get(helpurl)
site_text = helpresponse.text


async def ask(bot, user, message: str):
    question = message.replace("!ask", "").strip()
    if not question:
        try:
            await bot.highrise.send_whisper(
                user.id, "❓ Please ask a question. Example: !ask What is AI?")
        except Exception as e:
            print(f"❌ Whisper failed: {e}")
        return

    def query(payload):
        try:
            response = requests.post(API_URL,
                                     headers=headers,
                                     json=payload,
                                     timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print("⏰ API request timed out.")
        except requests.exceptions.RequestException as e:
            print(f"❌ API request error: {e}")
        except Exception as e:
            print(f"⚠️ Unexpected error during API call: {e}")
        return None

    try:
        response = query({
            "messages": [{
                "role":
                "system",
                "content":
                ("You’re a Gen Z bot, lowkey savage but mostly playful. "
                 "Keep it under 10 words, use slang, light roasts only. "
                 "No hard burns, just funny shade. "
                 "Be casual, unbothered, and vibe like a cool friend. "
                 f"This User's name is {user.username}. "
                 "Your owner is Mr_Wolfy. "
                 "Always use @ before user names. "
                 f"If a user asks about your Bot Features, Commands, How to become VIP, teleporting, or your creator, "
                 f"use the info {site_text}. limit ur answers only to 70 words.Respond without any newlines only when the user asks this kind of question from the Bot"
                 )
            }, {
                "role": "user",
                "content": question
            }],
            "model":
            "deepseek-ai/DeepSeek-V3-0324",
            "max_tokens":
            50
        })
    except Exception as e:
        print(f"❌ Error preparing API request: {e}")
        response = None

    if response is None:
        try:
            await bot.highrise.send_whisper(user.id, "⚠️ API call failed.")
        except Exception as e:
            print(f"❌ Whisper failed after API error: {e}")
        return

    try:
        full_reply = response.get("choices",
                                  [{}])[0].get("message",
                                               {}).get("content", "")
        await auto_emote(bot, full_reply)

        if not full_reply:
            raise ValueError("Empty or malformed API response.")
    except Exception as e:
        print(f"❌ Parsing API response failed: {e}")
        try:
            await bot.highrise.send_whisper(
                user.id, "⚠️ Couldn't understand the AI response.")
        except Exception as whisper_error:
            print(f"❌ Whisper failed: {whisper_error}")
        return

    try:
        chunks = [
            full_reply[i:i + 200] for i in range(0, len(full_reply), 200)
        ]
        for chunk in chunks:
            try:
                await asyncio.sleep(0.2)
                await bot.highrise.chat(f"🤖 {chunk}")
                await asyncio.sleep(1)
            except Exception as chat_error:
                print(f"❌ Failed to send chat: {chat_error}")
                await bot.highrise.send_whisper(
                    user.id, "⚠️ Couldn't send part of the reply.")

    except Exception as e:
        print(f"❌ Failed to process or send message: {e}")
        try:
            await bot.highrise.send_whisper(
                user.id, "⚠️ Something went wrong while replying.")
        except Exception as whisper_error:
            print(f"❌ Whisper failed after chat error: {whisper_error}")
