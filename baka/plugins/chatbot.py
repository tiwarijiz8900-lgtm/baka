import os
import random
import httpx
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from baka.config import GROQ_API_KEY, GROQ_URL, AI_MODEL

# ======================================================
# 🔥 SETTINGS & REPLIES
# ======================================================

CHAT_ALWAYS_ON = True

# Angel ki special lines
ANGEL_REPLIES = [
    "Ji meri jaan, bolo? 😘",
    "Angel hamesha tumhare saath hai baby.. ❤️",
    "Hukum kijiye mere hero, angel haazir hai 😇",
    "I love it when you call me Angel! 😍"
]

# ======================================================
# 🔥 FAST AI LOGIC (FIXES MISTRAL IMPORT ERROR)
# ======================================================

async def get_groq_response(text: str, user_name: str):
    """Mistral ko replace karke Groq AI se fast reply leta hai."""
    if not GROQ_API_KEY:
        return f"{user_name} jaan, admin ne API key nahi lagayi 😭"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # AI Instruction: Bahut chota aur sweet reply
    payload = {
        "model": AI_MODEL,
        "messages": [
            {
                "role": "system", 
                "content": f"Your name is Angel. You are talking to {user_name}. Keep your replies extremely short (max 10 words). Use romantic Hinglish and emojis."
            },
            {"role": "user", "content": text}
        ],
        "max_tokens": 40, # Isse reply chhota aur fast aayega
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
    """Har message pe unlimited fast reply + Name tagging."""
    if not CHAT_ALWAYS_ON:
        return

    msg = update.message
    if not msg or not msg.text or msg.text.startswith("/"):
        return

    # Member ka First Name lena
    user_name = msg.from_user.first_name
    incoming_text = msg.text.lower()

    # Typing action dikhana
    await context.bot.send_chat_action(msg.chat.id, ChatAction.TYPING)

    # Groq AI se reply lena (Purana Mistral system fix)
    api_reply = await get_groq_response(msg.text, user_name)

    # Angel Logic
    if "angel" in incoming_text:
        special_msg = random.choice(ANGEL_REPLIES)
        final_text = f"✨ **{user_name}**, {special_msg}\n\n{api_reply}"
    else:
        # Normal auto reply with Name
        final_text = f"🌸 **{user_name}**, {api_reply}"

    # Reply send karna
    await msg.reply_text(final_text, parse_mode="Markdown")
