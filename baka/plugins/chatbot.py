import os
import random
import httpx
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from baka.config import GROQ_API_KEY, GROQ_URL, AI_MODEL

# ======================================================
# 🔥 SETTINGS
# ======================================================

CHAT_ALWAYS_ON = True

# Angel ki sweet lines
ANGEL_REPLIES = [
    "Ji meri jaan, bolo? 😘",
    "Angel hamesha tumhare saath hai baby.. ❤️",
    "Hukum kijiye mere hero, angel haazir hai 😇",
    "I love it when you call me Angel! 😍"
]

# ======================================================
# 🔥 FAST & SHORT AI LOGIC
# ======================================================

async def get_groq_response(text: str, user_name: str):
    """Short and sweet AI reply logic."""
    if not GROQ_API_KEY:
        return f"{user_name} jaan, admin ne AI key nahi lagayi 😭"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # AI Instruction: Short reply + Hinglish
    payload = {
        "model": AI_MODEL,
        "messages": [
            {
                "role": "system", 
                "content": f"Your name is Angel. You are talking to {user_name}. Keep your replies very short (max 15-20 words). Speak in sweet romantic Hinglish. Use emojis."
            },
            {"role": "user", "content": text}
        ],
        "max_tokens": 50, # Isse reply chhota aur fast aayega
        "temperature": 0.8
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(GROQ_URL, headers=headers, json=payload)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return f"Thoda busy hoon {user_name}.. 😴"
    except Exception:
        return f"Net slow hai {user_name} baby 😭"

# ======================================================
# 🔥 MAIN AUTO REPLY (PRIVATE & GROUP)
# ======================================================

async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles unlimited auto replies with Name tagging."""
    if not CHAT_ALWAYS_ON:
        return

    msg = update.message
    if not msg or not msg.text or msg.text.startswith("/"):
        return

    # User ka First Name nikalna
    user_name = msg.from_user.first_name
    incoming_text = msg.text.lower()

    # Typing action start
    await context.bot.send_chat_action(msg.chat.id, ChatAction.TYPING)

    # Groq AI se reply lena
    api_reply = await get_groq_response(msg.text, user_name)

    # Angel Logic: Agar message mein 'angel' ho
    if "angel" in incoming_text:
        special_msg = random.choice(ANGEL_REPLIES)
        final_text = f"✨ **{user_name}** {special_msg}\n\n{api_reply}"
    else:
        # Normal Reply with Name shuruat mein
        final_text = f"🌸 **{user_name}**, {api_reply}"

    # Fast Reply
    await msg.reply_text(final_text, parse_mode="Markdown")

# ======================================================
# 🔥 COMMANDS
# ======================================================

async def chaton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ALWAYS_ON
    CHAT_ALWAYS_ON = True
    await update.message.reply_text("✅ Angel Auto-Chat ON! 😘")

async def chatoff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ALWAYS_ON
    CHAT_ALWAYS_ON = False
    await update.message.reply_text("❌ Angel Auto-Chat OFF! 😴")
