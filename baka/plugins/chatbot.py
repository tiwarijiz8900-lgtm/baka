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

# Normal text replies (bina kisi font ke)
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
    Note: Function ka naam 'ask_mistral_raw' hi rakha hai 
    taaki aapka Heroku crash na ho, lekin andar kaam GROQ hi karega.
    """
    if not GROQ_API_KEY:
        return f"{user_name}, admin ne Groq key nahi lagayi."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": AI_MODEL, # Groq model yahan config se aayega
        "messages": [
            {
                "role": "system", 
                "content": f"Your name is Angel. User: {user_name}. Use only normal text. No bold, no italic, no stylish fonts. Reply in very short Hinglish (5 words max). Be romantic and sweet."
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
                # Groq ka fast response return karega
                return response.json()['choices'][0]['message']['content']
            return "Server down hai baby. 😴"
    except Exception:
        return "Net issue hai, thoda wait karo. 😭"

# ======================================================
# 🔥 UNLIMITED AUTO REPLY HANDLER
# ======================================================

async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not CHAT_ALWAYS_ON:
        return

    msg = update.message
    if not msg or not msg.text or msg.text.startswith("/"):
        return

    # User name aur text (Simple format)
    user_name = msg.from_user.first_name
    incoming_text = msg.text.lower()

    # Bot ko typing dikhana
    await context.bot.send_chat_action(msg.chat.id, ChatAction.TYPING)

    # Groq se short reply mangwana
    api_reply = await ask_mistral_raw(msg.text, user_name)

    # Final Reply: Name + Reply (Normal Font)
    if "angel" in incoming_text:
        special = random.choice(ANGEL_REPLIES)
        final_text = f"{user_name}, {special}\n\n{api_reply}"
    else:
        final_text = f"{user_name}, {api_reply}"

    # Simple reply without markdown
    await msg.reply_text(final_text)
