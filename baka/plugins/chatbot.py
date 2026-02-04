import os
import random
import httpx
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from baka.config import GROQ_API_KEY, GROQ_URL, AI_MODEL

# ======================================================
# 🔥 SIMPLE SETTINGS (NO STYLISH FONTS)
# ======================================================

CHAT_ALWAYS_ON = True

ANGEL_REPLIES = [
    "Ji meri jaan, bolo? 😘",
    "Angel hamesha tumhare saath hai baby.. ❤️",
    "Hukum kijiye mere hero, angel haazir hai 😇",
    "I love it when you call me Angel! 😍"
]


# ======================================================
# 🔥 GROQ AI ENGINE (FAST & SHORT)
# ======================================================

async def ask_mistral_raw(text: str, user_name: str):
    """
    Groq AI reply function
    (Naam purposely same rakha hai taaki purana code break na ho)
    """

    if not GROQ_API_KEY:
        return f"{user_name}, admin ne Groq key nahi lagayi."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": AI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    f"Your name is Angel. User: {user_name}. "
                    "Reply only normal text. No bold. No stylish fonts. "
                    "Very short Hinglish (5 words max). Romantic and sweet."
                )
            },
            {"role": "user", "content": text}
        ],
        "max_tokens": 25,
        "temperature": 0.6
    }

    try:
        async with httpx.AsyncClient(timeout=7) as client:
            response = await client.post(GROQ_URL, headers=headers, json=payload)

            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']

            return "Server down hai baby 😴"

    except Exception:
        return "Net issue hai, thoda wait karo 😭"


# ======================================================
# 🔥 UNLIMITED AUTO REPLY HANDLER
# ======================================================

async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not CHAT_ALWAYS_ON:
        return

    msg = update.message

    if not msg or not msg.text or msg.text.startswith("/"):
        return

    user_name = msg.from_user.first_name
    incoming_text = msg.text.lower()

    await context.bot.send_chat_action(msg.chat.id, ChatAction.TYPING)

    api_reply = await ask_mistral_raw(msg.text, user_name)

    if "angel" in incoming_text:
        special = random.choice(ANGEL_REPLIES)
        final_text = f"{user_name}, {special}\n\n{api_reply}"
    else:
        final_text = f"{user_name}, {api_reply}"

    await msg.reply_text(final_text)


# ======================================================
# ✅🔥 CRASH FIX (VERY IMPORTANT)
# ======================================================
# Old plugins import: get_groq_response
# This line prevents Heroku crash

get_groq_response = ask_mistral_raw
