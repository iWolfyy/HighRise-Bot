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
from config import NEWS_API_KEY

highriseroomID = ROOM_ID


async def news(bot, user, message: str):
    url = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=5&apiKey={NEWS_API_KEY}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await bot.highrise.send_whisper(
                        user.id,
                        "⚠️ Failed to fetch news at the moment. Please try again later."
                    )
                    return
                data = await resp.json()
                articles = data.get("articles", [])
                if not articles:
                    await bot.highrise.send_whisper(
                        user.id, "ℹ️ No news headlines available right now.")
                    return

                # Build nicely formatted news message
                msg = "📰 **Top News Headlines** 📰\n" + "────────────────────────\n"
                for i, article in enumerate(articles, 1):
                    title = article.get("title", "No title")
                    source = article.get("source",
                                         {}).get("name", "Unknown Source")
                    # Clean up any trailing spaces, limit title length if needed
                    title = title.strip()
                    if len(title) > 100:
                        title = title[:97] + "..."
                    msg += f"🔹 {i}. {title}\n    — {source}\n\n"

                msg += "────────────────────────\n"
                msg += "💡 Stay informed with the latest updates!"

                # Split and send message chunks within 250 char limit
                chunks = split_message(msg, limit=250)
                for chunk in chunks:
                    await bot.highrise.send_whisper(user.id, chunk)
                    await asyncio.sleep(0.6
                                        )  # small delay to avoid rate limits

    except Exception as e:
        await bot.highrise.send_whisper(user.id, f"❌ Error fetching news: {e}")
        print(f"News command error: {e}")


def split_message(text, limit=250):
    lines = text.split("\n")
    chunks = []
    current = ""
    for line in lines:
        # +1 for newline char when joining lines
        if len(current) + len(line) + 1 > limit:
            chunks.append(current)
            current = line
        else:
            current += ("\n" if current else "") + line
    if current:
        chunks.append(current)
    return chunks
